# Docker Setup Guide

## 🐳 Using Docker

### What is Docker?
Docker allows you to run the application in a containerized environment - the same everywhere (Windows, Mac, Linux, Cloud).

---

## 📦 Installation

### Windows/Mac
1. Download **Docker Desktop** from https://www.docker.com/products/docker-desktop
2. Install and restart computer
3. Open PowerShell/Terminal and verify: `docker --version`

### Linux (Ubuntu)
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose -y
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🚀 Running with Docker

### Option 1: Simple Method
```bash
cd customer-lifetime-value-Prediction

# Build image
docker build -t clv-predictor .

# Run container
docker run -p 5000:5000 clv-predictor
```

Access: `http://localhost:5000`

### Option 2: Docker Compose (Recommended)
```bash
cd customer-lifetime-value-Prediction

# Start service
docker-compose up

# Stop service
docker-compose down
```

---

## 🔧 Docker Commands Reference

### Image Commands
```bash
# Build image
docker build -t clv-predictor .

# List images
docker images

# Remove image
docker rmi clv-predictor

# Push to Docker Hub
docker tag clv-predictor username/clv-predictor
docker push username/clv-predictor
```

### Container Commands
```bash
# Run container
docker run -p 5000:5000 clv-predictor

# Run in background
docker run -d -p 5000:5000 clv-predictor

# List running containers
docker ps

# View logs
docker logs container_id

# Stop container
docker stop container_id

# Remove container
docker rm container_id

# Interactive terminal
docker exec -it container_id bash
```

---

## 📱 Access from Other Devices

### Find Docker Host IP
```bash
# Windows/Mac
docker inspect -f "{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}" container_id

# Or use host machine IP
ipconfig  # Windows
ifconfig  # Mac/Linux
```

### Access from Android/iPhone
1. Connect to same WiFi
2. Get X.X.X.X IP address from above
3. Open: `http://X.X.X.X:5000`

---

## ☁️ Deploy Docker to Cloud

### Docker Hub
```bash
# Create Docker Hub account at hub.docker.com

# Login
docker login

# Tag image
docker tag clv-predictor:latest username/clv-predictor:latest

# Push
docker push username/clv-predictor:latest

# Pull on server
docker pull username/clv-predictor:latest
docker run -p 80:5000 username/clv-predictor:latest
```

### AWS (EC2)
```bash
# 1. SSH into EC2 instance
ssh -i key.pem ec2-user@instance-ip

# 2. Install Docker
sudo yum update -y
sudo yum install docker -y
sudo systemctl start docker

# 3. Pull and run
docker pull username/clv-predictor:latest
docker run -d -p 80:5000 username/clv-predictor:latest
```

### Google Cloud Run
```bash
# Build for Cloud Run
gcloud builds submit --tag gcr.io/PROJECT_ID/clv-predictor

# Deploy
gcloud run deploy clv-predictor \
  --image gcr.io/PROJECT_ID/clv-predictor \
  --platform managed \
  --memory 512Mi \
  --cpu 1
```

---

## 🔐 Production Setup

### Secure Docker Run
```bash
docker run \
  -d \
  -p 80:5000 \
  -e FLASK_ENV=production \
  --restart unless-stopped \
  --health-cmd='curl -f http://localhost:5000/health || exit 1' \
  --health-interval=30s \
  --health-timeout=10s \
  --health-retries=3 \
  username/clv-predictor:latest
```

### With Volume Mounting (Persist Data)
```bash
docker run -d \
  -p 5000:5000 \
  -v /data:/app/uploads \
  clv-predictor
```

### With Environment Variables
```bash
docker run -d \
  -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  clv-predictor
```

---

## 📊 Docker Compose Advanced

### Full Stack with Database
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:5000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/clv
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: clv
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - web

volumes:
  postgres_data:
```

---

## ⚠️ Troubleshooting

### "Cannot connect to Docker daemon"
- Start Docker Desktop (Windows/Mac)
- Start Docker service (Linux): `sudo systemctl start docker`

### "Port already in use"
```bash
# Kill process using port
docker stop container_id

# Or use different port
docker run -p 8080:5000 clv-predictor  # Use 8080 instead
```

### "Out of memory"
```bash
# Limit memory
docker run -m 512m -p 5000:5000 clv-predictor

# Or increase Docker Desktop memory settings
```

### "Slow performance"
```bash
# Check resource usage
docker stats

# Limit CPU
docker run --cpus=2 -p 5000:5000 clv-predictor
```

---

## 🎯 Benefits of Docker

✅ **Consistency**: Works same everywhere
✅ **Isolation**: No conflicts with system
✅ **Scalability**: Easy to deploy multiple instances
✅ **Portability**: Works on any OS
✅ **Simplicity**: No dependency issues

---

## 📚 Docker Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

**Happy Docker sailing! ⛵**
