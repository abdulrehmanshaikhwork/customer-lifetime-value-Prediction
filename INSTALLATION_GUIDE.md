# Installation Guide for All Devices

## 🖥️ Windows (Desktop/Laptop)

### Method 1: Simple Setup (Recommended)

**Step 1: Install Python**
1. Download from https://www.python.org/downloads/
2. ✅ Check "Add Python to PATH" during installation
3. Verify: Open Command Prompt, type `python --version`

**Step 2: Download Project**
```bash
git clone https://github.com/abdulrehmanshaikhwork/customer-lifetime-value-Prediction.git
cd customer-lifetime-value-Prediction
```
Or download ZIP from GitHub and extract

**Step 3: Install Requirements**
```bash
pip install -r requirements.txt
```

**Step 4: Run Application**
```bash
python app.py
```

**Step 5: Open in Browser**
- Type in address bar: `http://localhost:5000`
- Bookmark it for quick access

**Step 6: Stop Server**
- Press `CTRL + C` in Command Prompt

### Method 2: Using Virtual Environment (Professional)

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

### Create Windows Shortcut
**Create `run.bat`:**
```batch
@echo off
python app.py
pause
```
Double-click to run!

---

## 🐧 Linux (Ubuntu/Debian)

### Installation Steps

```bash
# 1. Update system
sudo apt-get update && sudo apt-get upgrade -y

# 2. Install Python & pip
sudo apt-get install python3 python3-pip -y

# 3. Clone repository
git clone https://github.com/abdulrehmanshaikhwork/customer-lifetime-value-Prediction.git
cd customer-lifetime-value-Prediction

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install requirements
pip install -r requirements.txt

# 6. Run application
python3 app.py
```

### Run in Background

```bash
# Install screen
sudo apt-get install screen -y

# Start in background
screen -S clv_app
python3 app.py

# Detach: Press Ctrl+A then D
# Reattach: screen -r clv_app
```

### Auto-start on System Boot

**Create `/etc/systemd/system/clv-predictor.service`:**
```ini
[Unit]
Description=CLV Predictor Service
After=network.target

[Service]
User=your_username
WorkingDirectory=/home/your_username/customer-lifetime-value-Prediction
ExecStart=/home/your_username/customer-lifetime-value-Prediction/venv/bin/python app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable service:**
```bash
sudo systemctl enable clv-predictor
sudo systemctl start clv-predictor
sudo systemctl status clv-predictor
```

---

## 🍎 macOS

### Installation Steps

```bash
# 1. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install Python
brew install python3

# 3. Clone repository
git clone https://github.com/abdulrehmanshaikhwork/customer-lifetime-value-Prediction.git
cd customer-lifetime-value-Prediction

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install requirements
pip install -r requirements.txt

# 6. Run
python3 app.py
```

### Create macOS Quick Launch

**Create `run.sh`:**
```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python3 app.py
open http://localhost:5000
```

Make executable:
```bash
chmod +x run.sh
```

Then double-click `run.sh`

---

## 📱 Android Phone/Tablet

### Method 1: Browser (Easiest)

**On Your Computer:**
1. Run `python app.py`
2. Open Command Prompt/Terminal, type: `ipconfig` (Windows) or `ifconfig` (Mac/Linux)
3. Find IPv4 address (example: 192.168.1.100)

**On Android Device:**
1. Connect to same WiFi network
2. Open Chrome/Firefox
3. Type in address bar: `http://192.168.1.100:5000`
4. Bookmark: Tap menu → Add to home screen

### Method 2: NGrok (Access from Anywhere)

```bash
# 1. Download from https://ngrok.com/download
# 2. Extract and run:
ngrok http 5000

# 3. Copy HTTPS link shown
# 4. Share with Android device
# 5. Open link in Chrome on Android
```

---

## 🍎 iPhone/iPad

### Using Safari

1. **On Your MacBook/PC:** Run `python app.py`
2. **Get IP:** Windows: `ipconfig`, Mac: `ifconfig`
3. **On iPhone:**
   - Open Safari
   - Type: `http://IP_ADDRESS:5000`
   - Tap Share → Add to Home Screen
   - Give it a name
   - Click Add

### PWA (Progressive Web App)

The app works as a PWA on modern iPhones!

---

## 🌐 Online Access (Anywhere)

### Option 1: Using Ngrok

```bash
# 1. Install ngrok
pip install pyngrok

# 2. Modify app.py:
from pyngrok import ngrok

# 3. Run
ngrok.connect(5000)

# 4. Share generated URL with anyone
```

### Option 2: Heroku Deployment

```bash
# 1. Create Heroku account (free at heroku.com)
# 2. Install Heroku CLI
# 3. Login
heroku login

# 4. Create app
heroku create your-app-name

# 5. Push code
git push heroku main

# 6. Open
heroku open

# Access from anywhere: https://your-app-name.herokuapp.com
```

---

## 🐳 Docker Desktop

### Windows/Mac/Linux

```bash
# 1. Install Docker Desktop
# https://www.docker.com/products/docker-desktop

# 2. Build image
docker build -t clv-predictor .

# 3. Run container
docker run -p 5000:5000 clv-predictor

# 4. Open browser
# http://localhost:5000

# 5. Access from other devices
# http://YOUR_IP:5000
```

---

## ☁️ Free Cloud Options

### Replit (Web-based)

1. Go to https://replit.com
2. Create account
3. Click "Create Repl" → Python
4. Paste code
5. Click Run
6. Share generated link with anyone

### PythonAnywhere

1. Sign up: https://www.pythonanywhere.com
2. Upload files
3. Create web app
4. Configure
5. Get live URL

### Railway.app

```bash
# 1. Create account
# 2. Create new project
# 3. Connect GitHub repo
# 4. Set start command: python app.py
# 5. Deploy
# 6. Get live URL
```

---

## 🔗 Network Setup Guide

### Find Your Computer's IP Address

**Windows:**
```powershell
ipconfig
```
Look for "IPv4 Address: 192.168.x.x"

**Mac/Linux:**
```bash
ifconfig
```
Look for "inet" address

### Access from Different Device

Replace `localhost` with your IP:
- Computer A: `http://localhost:5000`
- Computer B on same WiFi: `http://192.168.1.100:5000`
- Android on same WiFi: `http://192.168.1.100:5000`
- iPhone on same WiFi: `http://192.168.1.100:5000`

### Troubleshooting Connection

1. **Ping test:**
   ```bash
   ping 192.168.1.100
   ```

2. **Check firewall:** Allow Python through Windows Firewall

3. **Same WiFi:** Ensure all devices on same network

4. **Port open:** Server must be running (see terminal output)

---

## 🔥 Quick Command Reference

### Python Commands
```bash
python app.py              # Run app (Windows)
python3 app.py             # Run app (Mac/Linux)
python main.py             # Train model
pip install -r requirements.txt  # Install packages
```

### Network Commands
```bash
# Find IP
ipconfig                   # Windows
ifconfig                   # Mac/Linux

# Test connection
ping 192.168.1.100
```

### Docker Commands
```bash
docker build -t name .     # Build image
docker run -p 5000:5000 name  # Run container
docker ps                  # List containers
docker stop container_id   # Stop container
```

---

## ✅ Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Requirements installed
- [ ] Model file exists (clv_model_bundle.pkl)
- [ ] Server starts without errors
- [ ] Can access in browser
- [ ] Can make predictions
- [ ] File upload works
- [ ] Mobile device can access via IP

---

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| "Python not found" | Add Python to PATH, restart computer |
| "Port 5000 in use" | Change port in app.py or kill process using port |
| "Requirements install error" | Use `pip install --upgrade pip` first |
| "Model not loaded" | Run `python main.py` to train |
| "Cannot access from other device" | Check IP address, firewall, same WiFi |
| "File upload fails" | Check file format (CSV/Excel), file size |

---

## 📚 Next Steps

1. ✅ Get it running locally
2. ✅ Test on mobile device on same WiFi
3. ✅ Deploy to cloud if needed
4. ✅ Enable production settings
5. ✅ Configure database (optional)

**Happy predicting! 🎉**
