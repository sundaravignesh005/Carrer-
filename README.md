# AI-based Career Path & Company Recommendation System

A comprehensive machine learning system that recommends career paths and job opportunities based on student profiles.

## Features

- **Student Profile Analysis**: Collects academic scores, technical skills, and interests
- **ML-based Career Prediction**: Uses Decision Tree and Random Forest classifiers
- **Live Job Scraping**: Fetches real-time job postings from major job portals
- **Company Recommendations**: Provides up to 10 relevant job openings
- **Feedback System**: Collects user feedback for continuous improvement

## Project Structure

```
career/
├── data/
│   ├── career_data.csv          # Training dataset
│   └── feedback.csv             # User feedback data
├── models/
│   └── career_model.pkl         # Trained ML model
├── src/
│   ├── data_processing.py       # Data preprocessing module
│   ├── model.py                 # ML model training and prediction
│   ├── jobs_scraper.py          # Job scraping functionality
│   └── cli_interface.py         # Command-line interface
├── app.py                       # Flask API backend
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### CLI Interface
```bash
python src/cli_interface.py
```

### Flask API
```bash
python app.py
```

### Streamlit Web App
```bash
streamlit run streamlit_app.py
```

## API Endpoints

- `POST /predict` - Get career recommendation and job listings
- `POST /feedback` - Submit user feedback
- `GET /health` - Health check

## Technologies Used

- **Machine Learning**: scikit-learn, pandas, numpy
- **Web Scraping**: requests, BeautifulSoup
- **Backend**: Flask, Flask-CORS
- **Frontend**: Streamlit, HTML/CSS
- **Data Storage**: CSV files, joblib for model persistence
