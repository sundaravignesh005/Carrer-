"""
Test Script for Career Recommendation System

This script tests all components of the career recommendation system.
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Add src directory to path
sys.path.append('src')

from data_processing import CareerDataProcessor
from model import CareerRecommendationModel
from jobs_scraper import JobScraper

def test_data_processing():
    """Test data processing module."""
    print("🧪 Testing Data Processing Module...")
    
    try:
        processor = CareerDataProcessor()
        
        # Load data
        df = processor.load_data('data/career_data.csv')
        print(f"   ✅ Data loaded: {len(df)} rows, {len(df.columns)} columns")
        
        # Preprocess data
        X, y = processor.preprocess_data(df)
        print(f"   ✅ Data preprocessed: {X.shape[0]} samples, {X.shape[1]} features")
        
        # Test user input preprocessing
        user_input = {
            '10th_score': 85,
            '12th_score': 82,
            'ug_score': 78,
            'skills': 'Python,SQL,Statistics,ML',
            'interests': 'Research,Analysis,Development'
        }
        
        user_features = processor.preprocess_user_input(user_input)
        print(f"   ✅ User input preprocessed: {user_features.shape}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_model_training():
    """Test model training and prediction."""
    print("\n🧪 Testing ML Model Module...")
    
    try:
        processor = CareerDataProcessor()
        model = CareerRecommendationModel('random_forest')
        
        # Load and preprocess data
        df = processor.load_data('data/career_data.csv')
        X, y = processor.preprocess_data(df)
        
        # Train model
        results = model.train(X, y, processor.feature_columns)
        print(f"   ✅ Model trained: Accuracy = {results['accuracy']:.4f}")
        
        # Test prediction
        user_input = {
            '10th_score': 85,
            '12th_score': 82,
            'ug_score': 78,
            'skills': 'Python,SQL,Statistics,ML',
            'interests': 'Research,Analysis,Development'
        }
        
        user_features = processor.preprocess_user_input(user_input)
        prediction, confidence = model.predict(user_features)
        print(f"   ✅ Prediction: {prediction} (confidence: {confidence:.4f})")
        
        # Test top predictions
        top_predictions = model.predict_multiple(user_features, top_k=3)
        print(f"   ✅ Top predictions: {len(top_predictions)}")
        
        # Save model
        model.save_model()
        print(f"   ✅ Model saved successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_job_scraping():
    """Test job scraping module."""
    print("\n🧪 Testing Job Scraping Module...")
    
    try:
        scraper = JobScraper()
        
        # Test sample job scraping
        jobs = scraper.scrape_jobs("Data Scientist", "India", 5, use_sample=True)
        print(f"   ✅ Sample jobs scraped: {len(jobs)} jobs")
        
        # Test job data structure
        if jobs:
            job = jobs[0]
            required_fields = ['title', 'company', 'location', 'salary', 'apply_link', 'source']
            for field in required_fields:
                if field not in job:
                    print(f"   ❌ Missing field: {field}")
                    return False
            print(f"   ✅ Job data structure valid")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_end_to_end():
    """Test end-to-end functionality."""
    print("\n🧪 Testing End-to-End System...")
    
    try:
        # Initialize components
        processor = CareerDataProcessor()
        model = CareerRecommendationModel('random_forest')
        job_scraper = JobScraper()
        
        # Load and preprocess data
        df = processor.load_data('data/career_data.csv')
        X, y = processor.preprocess_data(df)
        
        # Train model
        model.train(X, y, processor.feature_columns)
        
        # Test user input
        user_input = {
            '10th_score': 85,
            '12th_score': 82,
            'ug_score': 78,
            'skills': 'Python,SQL,Statistics,ML',
            'interests': 'Research,Analysis,Development'
        }
        
        # Get prediction
        user_features = processor.preprocess_user_input(user_input)
        prediction, confidence = model.predict(user_features)
        
        # Get job recommendations
        jobs = job_scraper.scrape_jobs(
            job_title=prediction,
            location="India",
            max_jobs=5,
            use_sample=True
        )
        
        print(f"   ✅ End-to-end test successful:")
        print(f"      - Prediction: {prediction}")
        print(f"      - Confidence: {confidence:.4f}")
        print(f"      - Jobs found: {len(jobs)}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Career Recommendation System Tests")
    print("=" * 60)
    
    # Run tests
    tests = [
        test_data_processing,
        test_model_training,
        test_job_scraping,
        test_end_to_end
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("\n📝 Next Steps:")
    print("1. Run CLI: python src/cli_interface.py")
    print("2. Run Flask API: python app.py")
    print("3. Run Streamlit App: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()
