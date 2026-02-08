from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_FILE = "clv_model_bundle.pkl"
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clv_segment(clv):
    """Segment customers based on CLV prediction"""
    if clv < 1000:
        return "Low Value"
    elif clv < 2500:
        return "Medium Value"
    else:
        return "High Value"

def get_segment_color(segment):
    """Return color for segment visualization"""
    colors = {
        "Low Value": "#FF6B6B",
        "Medium Value": "#FFA500",
        "High Value": "#00D9A3"
    }
    return colors.get(segment, "#999999")

# Load the model at startup
def load_model():
    if os.path.exists(MODEL_FILE):
        bundle = joblib.load(MODEL_FILE)
        return bundle["model"], bundle["features"]
    else:
        raise FileNotFoundError(f"{MODEL_FILE} not found. Please train the model first using main.py")

try:
    loaded_model, features = load_model()
    model_loaded = True
except Exception as e:
    print(f"Warning: {e}")
    model_loaded = False

@app.route('/')
def index():
    """Serve the HTML interface"""
    return open('index.html', 'r', encoding='utf-8').read()

@app.route('/predict', methods=['POST'])
def predict():
    """
    Make CLV prediction based on Recency and Frequency
    Expected JSON: {"recency": float, "frequency": float}
    """
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded. Please train the model first using main.py'
        }), 500

    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'recency' not in data or 'frequency' not in data:
            return jsonify({
                'error': 'Missing required fields: recency and frequency'
            }), 400

        recency = float(data['recency'])
        frequency = float(data['frequency'])

        # Validate ranges
        if recency < 0 or frequency < 0:
            return jsonify({
                'error': 'Recency and Frequency must be non-negative'
            }), 400

        if frequency == 0:
            return jsonify({
                'error': 'Frequency must be at least 1'
            }), 400

        # Create feature dataframe
        input_data = pd.DataFrame({
            'Recency': [recency],
            'Frequency': [frequency]
        })

        # Make prediction
        prediction = loaded_model.predict(input_data)[0]

        # Ensure prediction is positive
        prediction = max(0, prediction)

        # Get segment
        segment = clv_segment(prediction)
        segment_color = get_segment_color(segment)

        return jsonify({
            'clv_prediction': float(prediction),
            'segment': segment,
            'segment_color': segment_color,
            'input': {
                'recency': recency,
                'frequency': frequency
            }
        })

    except ValueError as e:
        return jsonify({
            'error': f'Invalid input format: {str(e)}'
        }), 400
    except Exception as e:
        return jsonify({
            'error': f'Prediction error: {str(e)}'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'model_loaded': model_loaded,
        'features': features if model_loaded else None
    })

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """
    Make multiple CLV predictions at once
    Expected JSON: {"predictions": [{"recency": float, "frequency": float}, ...]}
    """
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded. Please train the model first using main.py'
        }), 500

    try:
        data = request.get_json()
        
        if not data or 'predictions' not in data:
            return jsonify({
                'error': 'Missing required field: predictions'
            }), 400

        predictions = data['predictions']
        
        if not isinstance(predictions, list):
            return jsonify({
                'error': 'predictions must be a list'
            }), 400

        results = []
        
        for item in predictions:
            if 'recency' not in item or 'frequency' not in item:
                return jsonify({
                    'error': 'Each prediction must have recency and frequency'
                }), 400

            recency = float(item['recency'])
            frequency = float(item['frequency'])

            if recency < 0 or frequency < 0:
                return jsonify({
                    'error': 'Recency and Frequency must be non-negative'
                }), 400

            if frequency == 0:
                return jsonify({
                    'error': 'Frequency must be at least 1'
                }), 400

            input_data = pd.DataFrame({
                'Recency': [recency],
                'Frequency': [frequency]
            })

            prediction = loaded_model.predict(input_data)[0]
            prediction = max(0, prediction)
            segment = clv_segment(prediction)
            segment_color = get_segment_color(segment)

            results.append({
                'clv_prediction': float(prediction),
                'segment': segment,
                'segment_color': segment_color,
                'input': {
                    'recency': recency,
                    'frequency': frequency
                }
            })

        return jsonify({
            'results': results,
            'count': len(results)
        })

    except Exception as e:
        return jsonify({
            'error': f'Batch prediction error: {str(e)}'
        }), 500

@app.route('/batch-upload', methods=['POST'])
def batch_upload():
    """
    Upload a CSV or Excel file with Recency and Frequency columns
    Returns predictions with segmentation
    """
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded. Please train the model first using main.py'
        }), 500

    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'error': 'No file provided'
            }), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({
                'error': 'No file selected'
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                'error': 'File type not allowed. Use CSV or Excel files'
            }), 400

        # Read the file
        try:
            if file.filename.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
        except Exception as e:
            return jsonify({
                'error': f'Failed to read file: {str(e)}'
            }), 400

        # Validate columns
        required_columns = ['Recency', 'Frequency']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return jsonify({
                'error': f'Missing required columns: {", ".join(missing_columns)}. File must contain "Recency" and "Frequency" columns'
            }), 400

        # Make predictions
        try:
            predictions = loaded_model.predict(df[required_columns])
            predictions = np.maximum(predictions, 0)  # Ensure non-negative

            # Create results dataframe
            results_df = df.copy()
            results_df['CLV_Prediction'] = predictions
            results_df['Segment'] = results_df['CLV_Prediction'].apply(clv_segment)

            # Convert to JSON
            results_json = results_df.to_dict(orient='records')

            # Generate summary statistics
            summary = {
                'total_customers': len(results_df),
                'average_clv': float(results_df['CLV_Prediction'].mean()),
                'min_clv': float(results_df['CLV_Prediction'].min()),
                'max_clv': float(results_df['CLV_Prediction'].max()),
                'segment_distribution': results_df['Segment'].value_counts().to_dict()
            }

            return jsonify({
                'results': results_json,
                'summary': summary,
                'count': len(results_df)
            })

        except Exception as e:
            return jsonify({
                'error': f'Prediction error: {str(e)}'
            }), 500

    except Exception as e:
        return jsonify({
            'error': f'Upload error: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Starting CLV Prediction API Server...")
    print("📍 Server running on http://localhost:5000")
    print("🌐 Open http://localhost:5000 in your browser")
    print("\nEndpoints:")
    print("  GET  /              - Web interface")
    print("  POST /predict       - Single prediction")
    print("  POST /batch-predict - Multiple predictions")
    print("  POST /batch-upload  - Upload CSV/Excel file for batch predictions")
    print("  GET  /health        - Health check")
    print("\nPress CTRL+C to stop the server")
    app.run(debug=True, port=5000)
