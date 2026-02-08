# Customer Lifetime Value Prediction 💰

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-Active-success)

A **production-ready web application** for predicting Customer Lifetime Value (CLV) using machine learning. Works on Windows, Linux, macOS, Android, iOS, and cloud platforms.

## 🌟 Features

✨ **Modern Web Interface**
- Beautiful, responsive HTML/CSS design
- Works on all browsers and devices
- Drag-and-drop file upload
- Real-time predictions

🤖 **Advanced ML Model**
- XGBoost regression algorithm
- Trained on RFM (Recency, Frequency, Monetary) analysis
- 80/20 train-test split with stratification
- High accuracy predictions

📊 **Analytics & Visualization**
- Interactive Chart.js graphs
- Segment distribution charts
- Summary statistics
- Customer segmentation (Low/Medium/High Value)

🚀 **Batch Processing**
- Single customer prediction
- Batch API for multiple customers
- CSV/Excel file upload processing
- Export results

## 📋 Quick Start

### Windows, Linux & macOS

#### 1. Clone Repository
```bash
git clone https://github.com/abdulrehmanshaikhwork/customer-lifetime-value-Prediction.git
cd customer-lifetime-value-Prediction
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Train Model (if needed)
```bash
python main.py
```

#### 4. Start Server
```bash
python app.py
```

#### 5. Open Browser
Navigate to: **http://localhost:5000**

---

## 🌐 Access on Different Devices

### Same Network (Windows/Linux/Mac to Any Device)

1. **Find your PC's IP address:**

   **Windows:**
   ```powershell
   ipconfig
   ```
   Look for "IPv4 Address" (e.g., 192.168.1.100)

   **Linux/Mac:**
   ```bash
   ifconfig
   ```

2. **Access from other devices:**
   - Replace `localhost:5000` with `YOUR_IP:5000`
   - Example: `http://192.168.1.100:5000`
   - Works on: Android, iPhone, Tablets, Other PCs

---

## 📱 Mobile Access

### Android
✅ **Works directly in browser:**
1. Open Chrome or Firefox
2. Go to: `http://YOUR_PC_IP:5000`
3. Bookmark for quick access

✅ **Create Android App (Optional):**
```html
<!-- Add to index.html <head> -->
<meta name="mobile-web-app-capable" content="yes">
<meta name="application-name" content="CLV Predictor">
<meta name="apple-mobile-web-app-capable" content="yes">
<link rel="icon" sizes="192x192" href="path-to-icon.png">
```

### iPhone/iPad
✅ **Works in Safari:**
1. Open Safari
2. Go to: `http://YOUR_PC_IP:5000`
3. Tap Share → Add to Home Screen

---

## 🐳 Docker Deployment

### Build & Run with Docker

#### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

#### 2. Create .dockerignore
```
.git
.gitignore
__pycache__
*.pyc
.DS_Store
uploads/*
```

#### 3. Build Image
```bash
docker build -t clv-predictor:latest .
```

#### 4. Run Container
```bash
docker run -p 5000:5000 -v $(pwd):/app clv-predictor:latest
```

#### 5. Access
- Local: `http://localhost:5000`
- Network: `http://HOST_IP:5000`

---

## ☁️ Cloud Deployment

### Heroku (Free)
```bash
heroku login
heroku create your-app-name
git push heroku main
heroku open
```

### AWS EC2
```bash
# 1. Launch Ubuntu instance
# 2. SSH into instance
ssh -i key.pem ubuntu@instance-ip

# 3. Install Python & dependencies
sudo apt-get update
sudo apt-get install python3-pip
pip install -r requirements.txt

# 4. Run with Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Google Cloud Run
```bash
# Create requirements.txt with gunicorn
# Deploy
gcloud run deploy clv-predictor --source . --platform managed

# Access
https://clv-predictor-xxxxx.run.app
```

### Azure App Service
```bash
az webapp create --resource-group mygroup --plan myplan --name clv-predictor
az webapp up --name clv-predictor
```

---

## 💻 System Requirements

### Minimum (Local)
- **RAM**: 2GB
- **Storage**: 500MB
- **Python**: 3.8+
- **Browser**: Chrome, Firefox, Safari, Edge

### Recommended (Server)
- **RAM**: 8GB
- **Storage**: 2GB
- **CPU**: 2+ cores
- **OS**: Linux (Ubuntu 20.04+)

---

## 🔧 Configuration

### Change Port
Edit `app.py` last line:
```python
app.run(debug=True, port=8080)  # Change 5000 to 8080
```

### Enable HTTPS (Production)
```python
app.run(ssl_context='adhoc')  # Install pyopenssl first
```

### Increase File Upload Size
```python
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
```

---

## 📚 API Documentation

### Single Prediction
```bash
POST http://localhost:5000/predict
Content-Type: application/json

{
    "recency": 30,
    "frequency": 5
}

Response:
{
    "clv_prediction": 450.75,
    "segment": "Medium Value",
    "segment_color": "#FFA500",
    "input": {
        "recency": 30,
        "frequency": 5
    }
}
```

### Batch Predictions
```bash
POST http://localhost:5000/batch-predict
Content-Type: application/json

{
    "predictions": [
        {"recency": 30, "frequency": 5},
        {"recency": 45, "frequency": 3}
    ]
}

Response:
{
    "results": [...],
    "count": 2
}
```

### File Upload
```bash
POST http://localhost:5000/batch-upload
Content-Type: multipart/form-data

file: (CSV or Excel file)

Response:
{
    "results": [...],
    "summary": {
        "total_customers": 100,
        "average_clv": 1250.50,
        "min_clv": 100.00,
        "max_clv": 5000.00,
        "segment_distribution": {...}
    },
    "count": 100
}
```

### Health Check
```bash
GET http://localhost:5000/health

Response:
{
    "status": "ok",
    "model_loaded": true,
    "features": ["Recency", "Frequency"]
}
```

---

## 🎯 Use Cases

### Single Prediction
- Quick lookup for one customer
- Sales team analysis
- Customer scoring

### Batch Predictions
- Weekly customer analysis
- Marketing campaign targeting
- Customer tier assignment

### File Upload
- Bulk customer analysis
- Import from CRM/ERP
- Historical data analysis

---

## 🔐 Security

### for Production:
```python
# 1. Hidden debug mode
app.run(debug=False)

# 2. Add authentication
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.login_required
@app.route('/predict', methods=['POST'])
def predict():
    ...
```

### Enable HTTPS
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with SSL
python app.py --ssl_context='adhoc'
```

---

## 🚀 Performance Optimization

### For High Traffic:

1. **Use Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Add Nginx Reverse Proxy**
```nginx
upstream flask_app {
    server 127.0.0.1:5000;
}

server {
    listen 80;
    
    location / {
        proxy_pass http://flask_app;
    }
}
```

3. **Enable Caching**
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

---

## 📖 Project Structure

```
customer-lifetime-value-Prediction/
├── app.py                    # Flask server
├── index.html                # Web interface
├── main.py                   # Model training
├── production_main.py        # Alternative models
├── clv_model_bundle.pkl      # Trained model
├── requirements.txt          # Dependencies
├── online_retail_II.xlsx     # Training data
├── test_clv.xlsx             # Test data
└── README.md                 # Documentation
```

---

## 🛠️ Troubleshooting

### "Port 5000 already in use"
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### "Model not found" error
```bash
python main.py  # Train model first
```

### "Cannot connect to server"
- Ensure `python app.py` is running
- Check firewall settings
- Use correct IP address (not localhost from other devices)

### Slow predictions
- Check system RAM usage
- Use Gunicorn instead of Flask development server
- Increase batch processing size

---

## 📊 Model Information

- **Algorithm**: XGBoost Regressor
- **Features**: Recency (days), Frequency (purchases)
- **Target**: Monetary (spending)
- **Training Data**: Online Retail II dataset
- **Model Size**: ~500KB

### Segmentation Thresholds
- **Low Value**: < $1,000
- **Medium Value**: $1,000 - $2,500
- **High Value**: > $2,500

---

## 🤝 Contributing

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "Add new feature"

# Push and create pull request
git push origin feature/new-feature
```

---

## 📄 License

MIT License - feel free to use for personal and commercial projects

---

## 👨‍💻 Author

**Abdul Rehman Shaikh**
- GitHub: [@abdulrehmanshaikhwork](https://github.com/abdulrehmanshaikhwork)
- Email: abdul@example.com

---

## 📞 Support

- 📧 Email: abdul@example.com
- 🐛 Issues: GitHub Issues
- 💬 Discussions: GitHub Discussions

---

## 🗓️ Changelog

### v1.0 (Feb 2026)
- ✅ Web interface launch
- ✅ Single & batch predictions
- ✅ File upload processing
- ✅ Customer segmentation
- ✅ Analytics dashboard
- ✅ Mobile responsive design

---

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [XGBoost Guide](https://xgboost.readthedocs.io/)
- [RFM Analysis](https://en.wikipedia.org/wiki/RFM_(customer_value))
- [Machine Learning Basics](https://scikit-learn.org/)

---

**Star ⭐ this repository if you find it helpful!**
