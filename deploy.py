"""
Deployment script for Vercel
This script handles the deployment configuration
"""

import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from model import CareerRecommendationModel
from data_processing import CareerDataProcessor
from jobs_scraper import JobScraper
from skills_gap_analysis import SkillsGapAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize components
model = CareerRecommendationModel()
processor = CareerDataProcessor()
job_scraper = JobScraper()
skills_analyzer = SkillsGapAnalyzer()

# Load the trained model
model.load_model()

@app.route('/')
def home():
    return jsonify({
        "message": "AI-Based Career Path Recommendation System",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        
        # Process user input
        user_features = processor.preprocess_user_input(data)
        
        # Make prediction
        prediction, confidence = model.predict(user_features)
        
        # Get job recommendations
        jobs = job_scraper.get_job_recommendations(prediction, limit=5)
        
        # Get skills gap analysis
        user_skills = data.get('skills', '').split(',')
        skills_analysis = skills_analyzer.analyze_skills_gap(user_skills, prediction)
        
        return jsonify({
            "prediction": prediction,
            "confidence": confidence,
            "jobs": jobs,
            "skills_analysis": skills_analysis
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/feedback', methods=['POST'])
def feedback():
    try:
        data = request.get_json()
        # Store feedback (implement as needed)
        return jsonify({"message": "Feedback received"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
