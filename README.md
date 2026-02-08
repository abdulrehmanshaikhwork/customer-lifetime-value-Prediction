# Customer Lifetime Value (CLV) Prediction Website

A modern web application for predicting customer lifetime value using machine learning.

## Features

✨ **Modern Web Interface** - Beautiful, responsive HTML website
🤖 **ML-Powered Predictions** - XGBoost machine learning model
📊 **RFM Analysis** - Uses Recency and Frequency metrics
⚡ **Real-time Predictions** - Instant CLV calculations
📱 **Mobile Friendly** - Works on all devices
🔄 **Batch Processing** - Predict for multiple customers at once

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the Model (If Not Already Done)

```bash
python main.py
```

This will:
- Read your `online_retail_II.xlsx` file
- Process customer transaction data
- Calculate RFM features
- Train an XGBoost model
- Save the model as `clv_model_bundle.pkl`

## Usage

### Start the Web Application

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

The website will:
1. Display a beautiful interface for entering customer data
2. Accept Recency (days since last purchase) and Frequency (number of purchases)
3. Show predicted Customer Lifetime Value instantly

### API Endpoints

#### Single Prediction
```bash
POST /predict
Content-Type: application/json

{
    "recency": 30,
    "frequency": 5
}
```

Response:
```json
{
    "clv_prediction": 450.75,
    "input": {
        "recency": 30,
        "frequency": 5
    }
}
```

#### Batch Predictions
```bash
POST /batch-predict
Content-Type: application/json

{
    "predictions": [
        {"recency": 30, "frequency": 5},
        {"recency": 45, "frequency": 3},
        {"recency": 10, "frequency": 12}
    ]
}
```

#### Health Check
```bash
GET /health
```

## Files

- **index.html** - Modern web interface (standalone, can be used offline with modifications)
- **app.py** - Flask backend API server
- **main.py** - Model training script
- **production_main.py** - Production model with multiple algorithms
- **requirements.txt** - Python dependencies

## Input Parameters

- **Recency (days)**: How many days since the customer made their last purchase
  - Range: 0-1000 days
  - Lower values = Recently purchased (good sign)

- **Frequency (purchases)**: Total number of purchases made by the customer
  - Range: 1-500 purchases
  - Higher values = More loyal customer

## Model Details

- **Algorithm**: XGBoost Regressor
- **Features Used**: Recency, Frequency
- **Target Variable**: Monetary (Total spending)
- **Training Set**: 80% of customer data
- **Test Set**: 20% of customer data
- **Stratification**: By CLV segments (quintiles)

## Troubleshooting

### "Model not loaded" error
- Make sure you've run `python main.py` first to train the model
- Check that `clv_model_bundle.pkl` exists in your directory

### "Cannot connect to server" error
- Make sure `app.py` is running
- Verify the server is on `http://localhost:5000`
- Check if port 5000 is already in use

### Port 5000 already in use
Run on a different port:
```bash
# Modify the last line in app.py:
app.run(debug=True, port=5001)  # Change port number
```

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## License

This project is provided as-is for educational and commercial use.

## Contact

For questions or issues, refer to the main project documentation.

---

**Happy predicting! 🎉**
