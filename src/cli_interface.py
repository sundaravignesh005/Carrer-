"""
Command Line Interface for Career Recommendation System

This module provides a CLI for testing the career recommendation system.
"""

import sys
import os
import json
from typing import Dict, Any, List
import logging

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processing import CareerDataProcessor
from model import CareerRecommendationModel
from jobs_scraper import JobScraper

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CareerCLI:
    """
    Command Line Interface for Career Recommendation System.
    """
    
    def __init__(self):
        self.processor = CareerDataProcessor()
        self.model = CareerRecommendationModel('random_forest')
        self.job_scraper = JobScraper()
        self.model_trained = False
    
    def print_header(self):
        """Print application header."""
        print("\n" + "="*60)
        print("🎯 AI-based Career Path & Company Recommendation System")
        print("="*60)
        print("Welcome! This system will help you find the perfect career path")
        print("based on your academic scores, skills, and interests.")
        print("="*60)
    
    def get_user_input(self) -> Dict[str, Any]:
        """
        Collect user input through CLI.
        
        Returns:
            Dict[str, Any]: User input data
        """
        print("\n📝 Please provide your information:")
        print("-" * 40)
        
        # Get academic scores
        print("\n📊 Academic Scores (0-100):")
        try:
            score_10th = float(input("10th Grade Percentage: ") or "0")
            score_12th = float(input("12th Grade Percentage: ") or "0")
            score_ug = float(input("UG/PG Percentage: ") or "0")
        except ValueError:
            print("⚠️  Invalid input. Using default scores (0).")
            score_10th = score_12th = score_ug = 0
        
        # Get skills
        print("\n💻 Technical Skills (comma-separated):")
        print("Examples: Python, Java, ML, SQL, Cloud, React, etc.")
        skills = input("Your skills: ").strip()
        
        # Get interests
        print("\n🎯 Interests (comma-separated):")
        print("Examples: Research, Development, Business, Analysis, etc.")
        interests = input("Your interests: ").strip()
        
        # Get location preference
        print("\n📍 Location Preference:")
        location = input("Preferred location (default: India): ").strip() or "India"
        
        # Get number of job recommendations
        print("\n🔢 Number of Job Recommendations:")
        try:
            max_jobs = int(input("How many jobs to show (default: 10): ") or "10")
        except ValueError:
            max_jobs = 10
        
        return {
            '10th_score': score_10th,
            '12th_score': score_12th,
            'ug_score': score_ug,
            'skills': skills,
            'interests': interests,
            'location': location,
            'max_jobs': max_jobs
        }
    
    def train_model(self):
        """Train the ML model."""
        try:
            print("\n🤖 Training ML model...")
            print("-" * 30)
            
            # Load and preprocess data
            df = self.processor.load_data('data/career_data.csv')
            X, y = self.processor.preprocess_data(df)
            
            # Train model
            results = self.model.train(X, y, self.processor.feature_columns)
            
            # Save model
            self.model.save_model()
            
            self.model_trained = True
            
            print(f"✅ Model trained successfully!")
            print(f"   Accuracy: {results['accuracy']:.4f}")
            print(f"   Cross-validation: {results['cv_mean']:.4f} (+/- {results['cv_std'] * 2:.4f})")
            
        except Exception as e:
            print(f"❌ Error training model: {e}")
            raise
    
    def get_career_prediction(self, user_data: Dict[str, Any]) -> tuple:
        """
        Get career prediction for user data.
        
        Args:
            user_data (Dict[str, Any]): User input data
            
        Returns:
            tuple: (prediction, confidence, top_predictions)
        """
        try:
            # Preprocess user input
            user_features = self.processor.preprocess_user_input(user_data)
            
            # Make prediction
            prediction, confidence = self.model.predict(user_features)
            
            # Get top predictions
            top_predictions = self.model.predict_multiple(user_features, top_k=3)
            
            return prediction, confidence, top_predictions
            
        except Exception as e:
            print(f"❌ Error getting prediction: {e}")
            raise
    
    def get_job_recommendations(self, job_title: str, location: str, max_jobs: int) -> List[Dict[str, Any]]:
        """
        Get job recommendations for the predicted career.
        
        Args:
            job_title (str): Job title to search for
            location (str): Location to search in
            max_jobs (int): Maximum number of jobs to fetch
            
        Returns:
            List[Dict[str, Any]]: List of job recommendations
        """
        try:
            print(f"\n🔍 Searching for {job_title} jobs in {location}...")
            
            # Use real job scraping from LinkedIn, Indeed, and Naukri
            jobs = self.job_scraper.scrape_jobs(
                job_title=job_title,
                location=location,
                max_jobs=max_jobs,
                use_sample=False  # Use real job scraping
            )
            
            return jobs
            
        except Exception as e:
            print(f"❌ Error getting job recommendations: {e}")
            return []
    
    def display_results(self, prediction: str, confidence: float, top_predictions: List, jobs: List[Dict[str, Any]]):
        """
        Display career prediction and job recommendations.
        
        Args:
            prediction (str): Predicted career
            confidence (float): Prediction confidence
            top_predictions (List): Top 3 predictions
            jobs (List[Dict[str, Any]]): Job recommendations
        """
        print("\n" + "="*60)
        print("🎯 YOUR CAREER RECOMMENDATION")
        print("="*60)
        
        # Display main prediction
        print(f"\n🏆 Recommended Career: {prediction}")
        print(f"   Confidence: {confidence:.2%}")
        
        # Display top predictions
        print(f"\n📊 Top Career Options:")
        for i, (career, conf) in enumerate(top_predictions, 1):
            print(f"   {i}. {career} ({conf:.2%})")
        
        # Display job recommendations
        if jobs:
            print(f"\n💼 JOB RECOMMENDATIONS ({len(jobs)} jobs found)")
            print("="*60)
            
            for i, job in enumerate(jobs, 1):
                print(f"\n{i}. {job['title']}")
                print(f"   🏢 Company: {job['company']}")
                print(f"   📍 Location: {job['location']}")
                print(f"   💰 Salary: {job['salary']}")
                print(f"   🔗 Apply: {job['apply_link']}")
                print(f"   📝 Description: {job['description'][:100]}...")
                print(f"   🌐 Source: {job['source']}")
        else:
            print("\n❌ No job recommendations found.")
    
    def collect_feedback(self, prediction: str, jobs: List[Dict[str, Any]]):
        """
        Collect user feedback.
        
        Args:
            prediction (str): Predicted career
            jobs (List[Dict[str, Any]]): Job recommendations
        """
        print("\n" + "="*60)
        print("📝 FEEDBACK")
        print("="*60)
        
        try:
            print(f"\nHow satisfied are you with the career recommendation '{prediction}'?")
            print("Rate from 1 (not satisfied) to 5 (very satisfied):")
            
            rating = int(input("Your rating (1-5): ") or "3")
            
            if rating < 1 or rating > 5:
                rating = 3
                print("⚠️  Invalid rating. Using default rating of 3.")
            
            comments = input("Any comments (optional): ").strip()
            
            # Save feedback
            feedback = {
                'timestamp': pd.Timestamp.now().isoformat(),
                'career': prediction,
                'rating': rating,
                'comments': comments,
                'total_jobs': len(jobs)
            }
            
            # Save to CSV
            import pandas as pd
            feedback_df = pd.DataFrame([feedback])
            
            if os.path.exists('data/feedback.csv'):
                feedback_df.to_csv('data/feedback.csv', mode='a', header=False, index=False)
            else:
                os.makedirs('data', exist_ok=True)
                feedback_df.to_csv('data/feedback.csv', index=False)
            
            print("✅ Thank you for your feedback!")
            
        except Exception as e:
            print(f"⚠️  Error saving feedback: {e}")
    
    def run(self):
        """Run the CLI application."""
        try:
            self.print_header()
            
            # Train model if needed
            if not self.model_trained:
                self.train_model()
            
            # Get user input
            user_data = self.get_user_input()
            
            # Get career prediction
            prediction, confidence, top_predictions = self.get_career_prediction(user_data)
            
            # Get job recommendations
            jobs = self.get_job_recommendations(
                job_title=prediction,
                location=user_data['location'],
                max_jobs=user_data['max_jobs']
            )
            
            # Display results
            self.display_results(prediction, confidence, top_predictions, jobs)
            
            # Collect feedback
            self.collect_feedback(prediction, jobs)
            
            print("\n" + "="*60)
            print("🎉 Thank you for using the Career Recommendation System!")
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            logger.error(f"CLI error: {e}")

def main():
    """Main function to run the CLI."""
    cli = CareerCLI()
    cli.run()

if __name__ == "__main__":
    main()
