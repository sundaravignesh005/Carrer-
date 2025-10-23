"""
Demo Script for Career Recommendation System

This script demonstrates the complete functionality of the career recommendation system.
"""

import sys
import os
import json
from datetime import datetime

# Add src directory to path
sys.path.append('src')

from data_processing import CareerDataProcessor
from model import CareerRecommendationModel
from jobs_scraper import JobScraper

def demo_career_recommendation():
    """Demonstrate the career recommendation system."""
    
    print("🎯 AI-based Career Path & Company Recommendation System Demo")
    print("=" * 70)
    
    # Initialize components
    print("\n📊 Initializing system components...")
    processor = CareerDataProcessor()
    model = CareerRecommendationModel('random_forest')
    job_scraper = JobScraper()
    
    # Load and preprocess data
    print("📈 Loading and preprocessing data...")
    df = processor.load_data('data/career_data.csv')
    X, y = processor.preprocess_data(df)
    
    # Train model
    print("🤖 Training ML model...")
    results = model.train(X, y, processor.feature_columns)
    print(f"   ✅ Model trained with accuracy: {results['accuracy']:.4f}")
    
    # Demo user profiles
    demo_profiles = [
        {
            'name': 'Alice - Data Science Enthusiast',
            'data': {
                '10th_score': 85,
                '12th_score': 82,
                'ug_score': 78,
                'skills': 'Python,SQL,Statistics,ML,Deep Learning',
                'interests': 'Research,Analysis,Development',
                'location': 'India'
            }
        },
        {
            'name': 'Bob - Full Stack Developer',
            'data': {
                '10th_score': 80,
                '12th_score': 77,
                'ug_score': 75,
                'skills': 'JavaScript,React,Node.js,HTML,CSS',
                'interests': 'Development,Design,Creativity',
                'location': 'India'
            }
        },
        {
            'name': 'Charlie - Business Analyst',
            'data': {
                '10th_score': 82,
                '12th_score': 79,
                'ug_score': 76,
                'skills': 'SQL,Excel,Power BI,Statistics',
                'interests': 'Business,Analysis,Problem Solving',
                'location': 'India'
            }
        }
    ]
    
    # Process each demo profile
    for i, profile in enumerate(demo_profiles, 1):
        print(f"\n{'='*70}")
        print(f"👤 DEMO PROFILE {i}: {profile['name']}")
        print(f"{'='*70}")
        
        # Get prediction
        user_features = processor.preprocess_user_input(profile['data'])
        prediction, confidence = model.predict(user_features)
        top_predictions = model.predict_multiple(user_features, top_k=3)
        
        # Display prediction
        print(f"\n🏆 Recommended Career: {prediction}")
        print(f"   Confidence: {confidence:.2%}")
        
        print(f"\n📊 Top Career Options:")
        for j, (career, conf) in enumerate(top_predictions, 1):
            print(f"   {j}. {career} ({conf:.2%})")
        
        # Get job recommendations
        print(f"\n💼 Job Recommendations:")
        jobs = job_scraper.scrape_jobs(
            job_title=prediction,
            location=profile['data']['location'],
            max_jobs=3,
            use_sample=True
        )
        
        for j, job in enumerate(jobs, 1):
            print(f"\n   {j}. {job['title']} - {job['company']}")
            print(f"      📍 {job['location']} | 💰 {job['salary']}")
            print(f"      🔗 {job['apply_link']}")
    
    # Display system statistics
    print(f"\n{'='*70}")
    print("📈 SYSTEM STATISTICS")
    print(f"{'='*70}")
    
    print(f"📊 Dataset Information:")
    print(f"   • Total students: {len(df)}")
    print(f"   • Career options: {df['Recommended_Career'].nunique()}")
    print(f"   • Features: {len(processor.feature_columns)}")
    
    print(f"\n🤖 Model Performance:")
    print(f"   • Accuracy: {results['accuracy']:.4f}")
    print(f"   • Cross-validation: {results['cv_mean']:.4f} (+/- {results['cv_std'] * 2:.4f})")
    
    # Feature importance
    feature_importance = model.get_feature_importance(5)
    if feature_importance:
        print(f"\n🔍 Top 5 Most Important Features:")
        for feature, importance in feature_importance:
            print(f"   • {feature}: {importance:.4f}")
    
    print(f"\n{'='*70}")
    print("🎉 Demo completed successfully!")
    print("=" * 70)
    
    print(f"\n📝 How to use the system:")
    print("1. CLI Interface: python src/cli_interface.py")
    print("2. Flask API: python app.py")
    print("3. Streamlit Web App: streamlit run streamlit_app.py")
    print("4. Run tests: python test_system.py")

if __name__ == "__main__":
    demo_career_recommendation()
