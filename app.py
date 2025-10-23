"""
Flask API Backend for Career Recommendation System

This module provides REST API endpoints for career recommendations and job listings.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List
import sys

# Add src directory to path
sys.path.append('src')

from data_processing import CareerDataProcessor
from model import CareerRecommendationModel
from jobs_scraper import JobScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize components
processor = CareerDataProcessor()
model = CareerRecommendationModel('random_forest')
job_scraper = JobScraper()

# Global variables
model_trained = False
feedback_data = []

def load_feedback_data():
    """Load feedback data from CSV file."""
    global feedback_data
    try:
        if os.path.exists('data/feedback.csv'):
            df = pd.read_csv('data/feedback.csv')
            feedback_data = df.to_dict('records')
        else:
            feedback_data = []
    except Exception as e:
        logger.error(f"Error loading feedback data: {e}")
        feedback_data = []

def save_feedback_data():
    """Save feedback data to CSV file."""
    try:
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(feedback_data)
        df.to_csv('data/feedback.csv', index=False)
        logger.info("Feedback data saved successfully")
    except Exception as e:
        logger.error(f"Error saving feedback data: {e}")

def train_model_if_needed():
    """Train model if not already trained."""
    global model_trained
    
    if not model_trained:
        try:
            # Load and preprocess data
            df = processor.load_data('data/career_data.csv')
            X, y = processor.preprocess_data(df)
            
            # Train model
            results = model.train(X, y, processor.feature_columns)
            
            # Save model
            model.save_model()
            
            model_trained = True
            logger.info("Model trained and saved successfully")
            
        except Exception as e:
            logger.error(f"Error training model: {e}")
            raise

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'model_trained': model_trained
    })

@app.route('/predict', methods=['POST'])
def predict_career():
    """
    Predict career and get job recommendations.
    
    Expected JSON payload:
    {
        "10th_score": 85,
        "12th_score": 82,
        "ug_score": 78,
        "skills": "Python,SQL,Statistics,ML",
        "interests": "Research,Analysis,Development",
        "location": "India",
        "max_jobs": 10
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['10th_score', '12th_score', 'ug_score', 'skills', 'interests']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Train model if needed
        train_model_if_needed()
        
        # Preprocess user input
        user_features = processor.preprocess_user_input(data)
        
        # Make prediction
        prediction, confidence = model.predict(user_features)
        
        # Get top predictions
        top_predictions = model.predict_multiple(user_features, top_k=3)
        
        # Get job recommendations
        location = data.get('location', 'India')
        max_jobs = data.get('max_jobs', 10)
        use_sample = data.get('use_sample', False)  # Use real job scraping by default
        
        jobs = job_scraper.scrape_jobs(
            job_title=prediction,
            location=location,
            max_jobs=max_jobs,
            use_sample=False  # Use real job scraping by default
        )
        
        # Prepare response
        response = {
            'prediction': {
                'career': prediction,
                'confidence': confidence,
                'top_predictions': [
                    {'career': career, 'confidence': conf} 
                    for career, conf in top_predictions
                ]
            },
            'job_recommendations': jobs,
            'metadata': {
                'total_jobs': len(jobs),
                'location': location,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        logger.error(f"Error in predict_career: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit user feedback for job recommendations.
    
    Expected JSON payload:
    {
        "career": "Data Scientist",
        "job_title": "Senior Data Scientist",
        "company": "TechCorp",
        "rating": 4,
        "comments": "Good match for my skills"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['career', 'rating']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate rating
        rating = data.get('rating')
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be an integer between 1 and 5'}), 400
        
        # Add feedback
        feedback_entry = {
            'timestamp': datetime.now().isoformat(),
            'career': data.get('career'),
            'job_title': data.get('job_title', ''),
            'company': data.get('company', ''),
            'rating': rating,
            'comments': data.get('comments', '')
        }
        
        feedback_data.append(feedback_entry)
        save_feedback_data()
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'feedback_id': len(feedback_data)
        })
        
    except Exception as e:
        logger.error(f"Error in submit_feedback: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/feedback', methods=['GET'])
def get_feedback():
    """Get all feedback data."""
    try:
        return jsonify({
            'feedback': feedback_data,
            'total_count': len(feedback_data)
        })
    except Exception as e:
        logger.error(f"Error in get_feedback: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/model/info', methods=['GET'])
def get_model_info():
    """Get model information and performance metrics."""
    try:
        if not model_trained:
            return jsonify({'error': 'Model not trained yet'}), 400
        
        # Get feature importance
        feature_importance = model.get_feature_importance(10)
        
        return jsonify({
            'model_type': model.model_type,
            'feature_columns': model.feature_columns,
            'top_features': [
                {'feature': feature, 'importance': importance} 
                for feature, importance in feature_importance
            ],
            'trained': model_trained
        })
        
    except Exception as e:
        logger.error(f"Error in get_model_info: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/jobs/sample', methods=['GET'])
def get_sample_jobs():
    """Get sample job data for testing."""
    try:
        job_title = request.args.get('title', 'Data Scientist')
        max_jobs = int(request.args.get('max_jobs', 10))
        
        jobs = job_scraper.get_sample_jobs(job_title, max_jobs)
        
        return jsonify({
            'jobs': jobs,
            'total_count': len(jobs)
        })
        
    except Exception as e:
        logger.error(f"Error in get_sample_jobs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/jobs/scrape', methods=['POST'])
def scrape_jobs():
    """
    Scrape jobs from job portals.
    
    Expected JSON payload:
    {
        "job_title": "Data Scientist",
        "location": "India",
        "max_jobs": 10,
        "use_sample": false
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        job_title = data.get('job_title', 'Data Scientist')
        location = data.get('location', 'India')
        max_jobs = data.get('max_jobs', 10)
        use_sample = data.get('use_sample', False)
        
        jobs = job_scraper.scrape_jobs(job_title, location, max_jobs, use_sample)
        
        return jsonify({
            'jobs': jobs,
            'total_count': len(jobs),
            'parameters': {
                'job_title': job_title,
                'location': location,
                'max_jobs': max_jobs,
                'use_sample': use_sample
            }
        })
        
    except Exception as e:
        logger.error(f"Error in scrape_jobs: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

def main():
    """Main function to run the Flask app."""
    # Load feedback data
    load_feedback_data()
    
    # Print available endpoints
    print("\n" + "="*50)
    print("Career Recommendation API")
    print("="*50)
    print("Available endpoints:")
    print("  GET  /health              - Health check")
    print("  POST /predict             - Get career prediction and job recommendations")
    print("  POST /feedback            - Submit feedback")
    print("  GET  /feedback            - Get all feedback")
    print("  GET  /model/info          - Get model information")
    print("  GET  /jobs/sample         - Get sample jobs")
    print("  POST /jobs/scrape         - Scrape jobs from portals")
    print("="*50)
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
