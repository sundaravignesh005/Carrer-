# 🚀 Career Recommendation System - Deployment Guide

Complete guide for setting up and deploying the enhanced career recommendation system.

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Docker Deployment](#docker-deployment)
7. [API Documentation](#api-documentation)
8. [Troubleshooting](#troubleshooting)

---

## 🔧 System Requirements

### Minimum Requirements:
- **Python**: 3.10 or higher
- **RAM**: 4GB (8GB recommended)
- **Disk Space**: 2GB
- **OS**: Windows, Linux, or macOS

### Optional:
- **Docker**: 20.10+ (for containerized deployment)
- **Redis**: For caching (production)

---

## ⚡ Quick Start

### 1. Clone and Setup

```bash
cd carrer
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
python migrate_to_database.py
```

### 3. Generate Expanded Dataset

```bash
python generate_expanded_dataset.py
```

### 4. Run the Application

```bash
# Option 1: Streamlit Web App
streamlit run streamlit_app.py

# Option 2: Flask API
python app.py

# Option 3: Admin Dashboard
streamlit run admin_dashboard.py
```

---

## 📦 Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Main Dependencies:**
- pandas, numpy, scikit-learn - Data processing & ML
- tensorflow, keras - Neural networks
- flask, streamlit - Web frameworks
- PyPDF2, python-docx - Resume parsing
- pyjwt, bcrypt - Authentication
- requests, beautifulsoup4 - Job scraping

### Step 2: Set Up Database

```bash
# Initialize database with migration
python migrate_to_database.py

# Expand dataset to 1000 samples
python generate_expanded_dataset.py
```

### Step 3: Configure Environment

Create a `.env` file in the root directory:

```env
# JWT Authentication
JWT_SECRET_KEY=your-secret-key-here-change-this

# Job API Keys (Optional)
RAPIDAPI_KEY=your-rapidapi-key
ADZUNA_APP_ID=your-adzuna-app-id
ADZUNA_APP_KEY=your-adzuna-app-key

# Email Configuration (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Email Display Name
FROM_EMAIL=your-email@gmail.com
FROM_NAME=Career Recommendation System
```

---

## ⚙️ Configuration

### Email Setup (Gmail)

1. **Enable 2FA** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account Settings
   - Security → 2-Step Verification
   - App passwords → Generate new
3. **Add to .env**:
   ```env
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=generated-app-password
   ```

### Job API Setup

#### RapidAPI (Recommended)
1. Sign up at [RapidAPI.com](https://rapidapi.com/)
2. Subscribe to **JSearch API** (free tier available)
3. Copy your API key to `.env`

#### Adzuna
1. Register at [Adzuna Developer](https://developer.adzuna.com/)
2. Create an application
3. Add App ID and Key to `.env`

---

## 🏃 Running the Application

### Method 1: Streamlit Web App (Recommended)

```bash
streamlit run streamlit_app.py
```

- **URL**: http://localhost:8501
- **Features**: 
  - Career prediction
  - Job search
  - Skills gap analysis
  - Salary prediction
  - Career roadmap

### Method 2: Flask API

```bash
python app.py
```

- **URL**: http://localhost:5000
- **API Endpoints**:
  - `POST /predict` - Career prediction
  - `POST /feedback` - Submit feedback
  - `GET /health` - Health check
  - `GET /model/info` - Model information

### Method 3: Admin Dashboard

```bash
streamlit run admin_dashboard.py
```

- **URL**: http://localhost:8502
- **Default Login**: 
  - Email: `admin@example.com`
  - Password: `admin123`

### Method 4: All Services

```bash
# Terminal 1: API
python app.py

# Terminal 2: Main App
streamlit run streamlit_app.py

# Terminal 3: Admin Dashboard
streamlit run admin_dashboard.py
```

---

## 🐳 Docker Deployment

### Quick Start with Docker Compose

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Services:**
- API: http://localhost:5000
- Streamlit: http://localhost:8501
- Admin: http://localhost:8502
- Redis: localhost:6379

### Individual Service Deployment

```bash
# Build image
docker build -t career-system .

# Run API
docker run -p 5000:5000 career-system python app.py

# Run Streamlit
docker run -p 8501:8501 career-system streamlit run streamlit_app.py

# Run Admin Dashboard
docker run -p 8502:8502 career-system streamlit run admin_dashboard.py
```

### Production Docker Deployment

```bash
# With environment file
docker-compose --env-file .env.production up -d

# With custom configuration
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose up -d --scale api=3
```

---

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

### Career Prediction

```http
POST /predict
Content-Type: application/json

{
  "10th_score": 85,
  "12th_score": 82,
  "ug_score": 78,
  "skills": "Python,SQL,Statistics,ML",
  "interests": "Research,Analysis,Development",
  "location": "India",
  "max_jobs": 10
}
```

**Response:**
```json
{
  "prediction": {
    "career": "Data Scientist",
    "confidence": 0.85,
    "top_predictions": [...]
  },
  "job_recommendations": [...],
  "metadata": {...}
}
```

### Skills Gap Analysis

```http
POST /api/skills/gap
Content-Type: application/json
Authorization: Bearer <token>

{
  "current_skills": ["Python", "SQL"],
  "target_career": "Data Scientist"
}
```

### Salary Prediction

```http
POST /api/salary/predict
Content-Type: application/json

{
  "career": "Data Scientist",
  "experience_years": 3,
  "location": "Bangalore",
  "skills": ["Python", "ML", "SQL"],
  "education": "Master"
}
```

---

## 🔍 Testing

### Run Unit Tests

```bash
# Test database
python -m pytest tests/test_database.py

# Test authentication
python -m pytest tests/test_auth.py

# Test ML models
python -m pytest tests/test_models.py

# Run all tests
python -m pytest tests/
```

### Test Individual Modules

```bash
# Test resume parser
python src/resume_parser.py

# Test salary predictor
python src/salary_predictor.py

# Test skills gap analyzer
python src/skills_gap_analysis.py

# Test career roadmap
python src/career_roadmap.py

# Test job API client
python src/job_api_client.py

# Test email service
python src/email_service.py
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. Database Error

```bash
# Reset database
python migrate_to_database.py --reset

# Check database integrity
sqlite3 data/career_system.db ".schema"
```

#### 2. TensorFlow Installation Issues

```bash
# For CPU-only
pip install tensorflow-cpu==2.15.0

# For Apple Silicon
pip install tensorflow-macos tensorflow-metal
```

#### 3. Port Already in Use

```bash
# Kill process on port
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

#### 4. Module Import Errors

```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 5. Docker Issues

```bash
# Clean Docker
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache

# Check logs
docker-compose logs api
```

---

## 🚀 Performance Optimization

### 1. Enable Caching

```python
# In app.py
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0'
})
```

### 2. Database Optimization

```bash
# Add indexes
sqlite3 data/career_system.db "CREATE INDEX idx_predictions_user ON predictions(user_id);"
```

### 3. Model Optimization

```python
# Use model caching
@st.cache_resource
def load_model():
    return model.load_model()
```

---

## 📊 Monitoring

### Health Checks

```bash
# API health
curl http://localhost:5000/health

# Streamlit health
curl http://localhost:8501/_stcore/health
```

### Logs

```bash
# View application logs
tail -f logs/app.log

# Docker logs
docker-compose logs -f api

# Filter logs
docker-compose logs api | grep ERROR
```

---

## 🔒 Security Best Practices

1. **Change default credentials** in production
2. **Use strong JWT secret keys**
3. **Enable HTTPS** in production
4. **Implement rate limiting**
5. **Regular security updates**
6. **Backup database regularly**
7. **Use environment variables** for secrets
8. **Enable CORS** only for trusted domains

---

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.yml
services:
  api:
    deploy:
      replicas: 3
```

### Load Balancing

```nginx
# nginx.conf
upstream api_backend {
    server localhost:5000;
    server localhost:5001;
    server localhost:5002;
}
```

### Database Scaling

```bash
# Switch to PostgreSQL for production
pip install psycopg2-binary
```

---

## 📞 Support

For issues or questions:
- Check the README.md
- Review PROJECT_SUMMARY.md
- Check troubleshooting section
- Create an issue on GitHub

---

## 🎉 Success!

Your Career Recommendation System is now ready for deployment!

**Next Steps:**
1. Configure your environment variables
2. Set up email notifications
3. Configure job APIs
4. Deploy to production
5. Monitor and maintain

Happy Deploying! 🚀

