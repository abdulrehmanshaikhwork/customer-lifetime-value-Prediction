# API & Integration Guide

## 🔌 REST API Reference

The CLV Predictor provides a complete REST API for integration with other applications.

---

## 🚀 Base URL

```
http://localhost:5000
```

For production, replace with your server IP/domain.

---

## 📊 Endpoints

### 1. Single Prediction

**Endpoint:** `POST /predict`

**Description:** Get CLV prediction for a single customer

**Request:**
```json
{
    "recency": 30,
    "frequency": 5
}
```

**Response (200 OK):**
```json
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

**Error Response (400):**
```json
{
    "error": "Missing required fields: recency and frequency"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"recency": 30, "frequency": 5}'
```

**Python Example:**
```python
import requests

response = requests.post('http://localhost:5000/predict', json={
    'recency': 30,
    'frequency': 5
})

data = response.json()
print(f"CLV Prediction: ${data['clv_prediction']}")
print(f"Segment: {data['segment']}")
```

**JavaScript Example:**
```javascript
const response = await fetch('http://localhost:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recency: 30, frequency: 5 })
});

const data = await response.json();
console.log(`CLV: $${data.clv_prediction}`);
```

---

### 2. Batch Predictions

**Endpoint:** `POST /batch-predict`

**Description:** Get CLV predictions for multiple customers at once

**Request:**
```json
{
    "predictions": [
        {"recency": 30, "frequency": 5},
        {"recency": 45, "frequency": 3},
        {"recency": 15, "frequency": 12}
    ]
}
```

**Response (200 OK):**
```json
{
    "results": [
        {
            "clv_prediction": 450.75,
            "segment": "Medium Value",
            "segment_color": "#FFA500",
            "input": {"recency": 30, "frequency": 5}
        },
        {
            "clv_prediction": 320.50,
            "segment": "Low Value",
            "segment_color": "#FF6B6B",
            "input": {"recency": 45, "frequency": 3}
        },
        {
            "clv_prediction": 2800.25,
            "segment": "High Value",
            "segment_color": "#00D9A3",
            "input": {"recency": 15, "frequency": 12}
        }
    ],
    "count": 3
}
```

**Python Example:**
```python
import requests

customers = [
    {'recency': 30, 'frequency': 5},
    {'recency': 45, 'frequency': 3},
    {'recency': 15, 'frequency': 12}
]

response = requests.post('http://localhost:5000/batch-predict', json={
    'predictions': customers
})

predictions = response.json()
for i, pred in enumerate(predictions['results']):
    print(f"Customer {i+1}: ${pred['clv_prediction']} ({pred['segment']})")
```

---

### 3. File Upload

**Endpoint:** `POST /batch-upload`

**Description:** Upload CSV or Excel file with customer data

**Request:** (multipart/form-data)
```
file: customers.csv
```

**Sample CSV Content:**
```csv
Recency,Frequency
30,5
45,3
15,12
60,1
```

**Response (200 OK):**
```json
{
    "results": [
        {
            "Recency": 30,
            "Frequency": 5,
            "CLV_Prediction": 450.75,
            "Segment": "Medium Value"
        },
        // ... more results
    ],
    "summary": {
        "total_customers": 100,
        "average_clv": 1250.50,
        "min_clv": 100.00,
        "max_clv": 5000.00,
        "segment_distribution": {
            "Low Value": 23,
            "Medium Value": 54,
            "High Value": 23
        }
    },
    "count": 100
}
```

**Python Example:**
```python
import requests

files = {'file': open('customers.csv', 'rb')}
response = requests.post('http://localhost:5000/batch-upload', files=files)

data = response.json()
print(f"Processed {data['count']} customers")
print(f"Average CLV: ${data['summary']['average_clv']}")
```

**JavaScript Example:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:5000/batch-upload', {
    method: 'POST',
    body: formData
});

const data = await response.json();
console.log(`Processed ${data.count} customers`);
```

---

### 4. Health Check

**Endpoint:** `GET /health`

**Description:** Check if server and model are running

**Response (200 OK):**
```json
{
    "status": "ok",
    "model_loaded": true,
    "features": ["Recency", "Frequency"]
}
```

**Use Case:** Monitor server health, API uptime

---

## 📝 Error Codes

| Code | Error | Meaning |
|------|-------|---------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid parameters |
| 500 | Server Error | Model not loaded or server issue |

---

## 🔐 Authentication

### Add Basic Auth

**Modify `app.py`:**
```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    return username == "admin" and password == "secret"

@app.route('/predict', methods=['POST'])
@auth.login_required
def predict():
    # ... existing code
```

**Request with Auth:**
```bash
curl -u admin:secret -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"recency": 30, "frequency": 5}'
```

---

## 🔗 Integration Examples

### Salesforce (Using Apex)

```apex
HttpRequest req = new HttpRequest();
req.setEndpoint('https://your-server.com/predict');
req.setMethod('POST');
req.setHeader('Content-Type', 'application/json');

Map<String, Object> body = new Map<String, Object>();
body.put('recency', 30);
body.put('frequency', 5);

req.setBody(JSON.serialize(body));

Http http = new Http();
HttpResponse res = http.send(req);

Map<String, Object> result = (Map<String, Object>) JSON.deserializeUntyped(res.getBody());
System.debug(result.get('clv_prediction'));
```

### HubSpot (Using Webhooks)

```javascript
// HubSpot custom code (NodeJS)
const axios = require('axios');

async function updateCLV(recency, frequency) {
    const response = await axios.post('https://your-server.com/predict', {
        recency: recency,
        frequency: frequency
    });
    
    return response.data.clv_prediction;
}
```

### Google Sheets

```javascript
function getCLV(recency, frequency) {
  const url = "https://your-server.com/predict";
  const payload = {
    recency: recency,
    frequency: frequency
  };
  
  const options = {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify(payload)
  };
  
  const response = UrlFetchApp.fetch(url, options);
  const result = JSON.parse(response.getContentText());
  return result.clv_prediction;
}
```

### Power BI (Using Web.Contents)

```powerquery
let
    Source = Json.Document(
        Web.Contents(
            "https://your-server.com/predict",
            [
                Content = Text.ToBinary("{""recency"":30,""frequency"":5}"),
                Headers = [#"Content-Type" = "application/json"]
            ]
        )
    )
in
    Source
```

---

## 📊 Data Mapping

### Input Parameters

| Parameter | Type | Range | Description |
|-----------|------|-------|-------------|
| recency | float | 0-1000 | Days since last purchase |
| frequency | float | 1-500 | Number of purchases |

### Output Fields

| Field | Type | Description |
|-------|------|-------------|
| clv_prediction | float | Predicted customer lifetime value ($) |
| segment | string | Customer segment (Low/Medium/High Value) |
| segment_color | string | Hex color for visualization |

---

## ⚡ Rate Limiting

For production, add rate limiting:

```python
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/predict', methods=['POST'])
@limiter.limit("100 per hour")
def predict():
    # ... code
```

---

## 🧪 Testing

### Using Postman

1. Create new POST request
2. URL: `http://localhost:5000/predict`
3. Body (JSON):
   ```json
   {
       "recency": 30,
       "frequency": 5
   }
   ```
4. Send

### Using Pytest

```python
import pytest
from app import app

@pytest.fixture
def client():
    return app.test_client()

def test_predict(client):
    response = client.post('/predict', json={
        'recency': 30,
        'frequency': 5
    })
    assert response.status_code == 200
    assert 'clv_prediction' in response.json
```

---

## 📱 Mobile Integration

### iOS (Swift)

```swift
struct PredictionRequest: Codable {
    let recency: Float
    let frequency: Float
}

struct PredictionResponse: Codable {
    let clv_prediction: Float
    let segment: String
}

func predictCLV(recency: Float, frequency: Float) {
    let url = URL(string: "http://YOUR_IP:5000/predict")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = PredictionRequest(recency: recency, frequency: frequency)
    request.httpBody = try JSONEncoder().encode(body)
    
    URLSession.shared.dataTask(with: request) { data, _, error in
        let response = try JSONDecoder().decode(PredictionResponse.self, from: data!)
        print("CLV: $\(response.clv_prediction)")
    }.resume()
}
```

### Android (Kotlin)

```kotlin
data class PredictionRequest(val recency: Float, val frequency: Float)
data class PredictionResponse(val clv_prediction: Float, val segment: String)

fun predictCLV(recency: Float, frequency: Float) {
    val retrofit = Retrofit.Builder()
        .baseUrl("http://YOUR_IP:5000")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    
    val service = retrofit.create(PredictionsService::class.java)
    val response = service.predict(PredictionRequest(recency, frequency))
}
```

---

## 📚 Documentation

For more details, see:
- `README.md` - Main documentation
- `FULL_GUIDE.md` - Complete guide
- `INSTALLATION_GUIDE.md` - Setup instructions
- `DOCKER_GUIDE.md` - Docker deployment

---

**Start integrating! 🚀**
