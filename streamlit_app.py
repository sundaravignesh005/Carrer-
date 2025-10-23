"""
Streamlit Web App for Career Recommendation System

This module provides a web interface for the career recommendation system.
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import sys
import os
from datetime import datetime
import requests
import logging

# Add src directory to path
sys.path.append('src')

from data_processing import CareerDataProcessor
from model import CareerRecommendationModel
from jobs_scraper import JobScraper
from salary_predictor import SalaryPredictor
from skills_gap_analysis import SkillsGapAnalyzer
from career_roadmap import CareerRoadmapGenerator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="AI Career Recommendation System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .prediction-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .job-card {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and cache the career dataset."""
    try:
        processor = CareerDataProcessor()
        df = processor.load_data('data/career_data.csv')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_resource
def load_model():
    """Load and cache the trained model."""
    try:
        processor = CareerDataProcessor()
        model = CareerRecommendationModel('random_forest')
        
        # Load data and train model
        df = processor.load_data('data/career_data.csv')
        X, y = processor.preprocess_data(df)
        
        # Train model
        model.train(X, y, processor.feature_columns)
        
        return processor, model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

def main():
    """Main Streamlit application."""
    
    # Header
    st.markdown('<h1 class="main-header">🎯 AI Career Recommendation System</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("📊 System Information")
    
    # Load data and model
    with st.spinner("Loading data and training model..."):
        df = load_data()
        processor, model = load_model()
    
    if df is None or processor is None or model is None:
        st.error("Failed to load data or model. Please check the data files.")
        return
    
    # Display dataset info
    st.sidebar.metric("Total Students", len(df))
    st.sidebar.metric("Career Options", df['Recommended_Career'].nunique())
    st.sidebar.metric("Features", len(processor.feature_columns))
    
    # Main content
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 Career Prediction", 
        "💰 Salary Prediction", 
        "📊 Skills Gap Analysis",
        "🗺️ Career Roadmap",
        "💼 Job Search", 
        "📈 Model Info"
    ])
    
    with tab1:
        st.header("Get Your Career Recommendation")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📝 Your Information")
            
            # Academic scores
            st.write("**Academic Scores (0-100):**")
            score_10th = st.slider("10th Grade Percentage", 0, 100, 85)
            score_12th = st.slider("12th Grade Percentage", 0, 100, 82)
            score_ug = st.slider("UG/PG Percentage", 0, 100, 78)
            
            # Skills
            st.write("**Technical Skills:**")
            skills_input = st.text_area(
                "Enter your skills (comma-separated)",
                value="Python, SQL, Statistics, ML",
                help="Examples: Python, Java, ML, SQL, Cloud, React, etc."
            )
            
            # Interests
            st.write("**Interests:**")
            interests_input = st.text_area(
                "Enter your interests (comma-separated)",
                value="Research, Analysis, Development",
                help="Examples: Research, Development, Business, Analysis, etc."
            )
            
            # Location
            location = st.text_input("Preferred Location", value="India")
            
            # Max jobs
            max_jobs = st.slider("Number of Job Recommendations", 1, 20, 10)
        
        with col2:
            st.subheader("🎯 Prediction Results")
            
            if st.button("Get Career Recommendation", type="primary"):
                try:
                    # Prepare user data
                    user_data = {
                        '10th_score': score_10th,
                        '12th_score': score_12th,
                        'ug_score': score_ug,
                        'skills': skills_input,
                        'interests': interests_input,
                        'location': location,
                        'max_jobs': max_jobs
                    }
                    
                    # Get prediction
                    user_features = processor.preprocess_user_input(user_data)
                    prediction, confidence = model.predict(user_features)
                    top_predictions = model.predict_multiple(user_features, top_k=3)
                    
                    # Display main prediction
                    st.markdown(f"""
                    <div class="prediction-card">
                        <h3>🏆 Recommended Career</h3>
                        <h2 style="color: #1f77b4;">{prediction}</h2>
                        <p><strong>Confidence:</strong> {confidence:.2%}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display top predictions
                    st.write("**Top Career Options:**")
                    for i, (career, conf) in enumerate(top_predictions, 1):
                        st.write(f"{i}. **{career}** ({conf:.2%})")
                    
                    # Get job recommendations
                    job_scraper = JobScraper()
                    jobs = job_scraper.scrape_jobs(
                        job_title=prediction,
                        location=location,
                        max_jobs=max_jobs,
                        use_sample=False  # Use real job scraping
                    )
                    
                    # Display job recommendations
                    if jobs:
                        st.write(f"**💼 Job Recommendations ({len(jobs)} jobs):**")
                        for i, job in enumerate(jobs, 1):
                            with st.expander(f"{i}. {job['title']} - {job['company']}"):
                                st.write(f"**Company:** {job['company']}")
                                st.write(f"**Location:** {job['location']}")
                                st.write(f"**Salary:** {job['salary']}")
                                st.write(f"**Description:** {job['description']}")
                                st.write(f"**Apply:** [Click here]({job['apply_link']})")
                                st.write(f"**Source:** {job['source']}")
                    
                    # Feedback section
                    st.write("**📝 Feedback:**")
                    rating = st.slider("Rate this recommendation (1-5)", 1, 5, 3)
                    comments = st.text_area("Comments (optional)")
                    
                    if st.button("Submit Feedback"):
                        # Save feedback
                        feedback = {
                            'timestamp': datetime.now().isoformat(),
                            'career': prediction,
                            'rating': rating,
                            'comments': comments,
                            'total_jobs': len(jobs)
                        }
                        
                        # Save to CSV
                        feedback_df = pd.DataFrame([feedback])
                        if os.path.exists('data/feedback.csv'):
                            feedback_df.to_csv('data/feedback.csv', mode='a', header=False, index=False)
                        else:
                            os.makedirs('data', exist_ok=True)
                            feedback_df.to_csv('data/feedback.csv', index=False)
                        
                        st.success("Thank you for your feedback!")
                
                except Exception as e:
                    st.error(f"Error getting recommendation: {e}")
    
    with tab2:
        st.header("💰 Salary Prediction")
        
        st.write("Predict salary based on career, experience, skills, and location")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Your Details")
            
            career_for_salary = st.selectbox(
                "Select Career",
                ["Data Scientist", "Machine Learning Engineer", "Software Developer",
                 "Full Stack Developer", "Data Analyst", "DevOps Engineer",
                 "Cloud Engineer", "Web Developer", "Mobile Developer",
                 "UI/UX Developer", "Business Analyst", "Product Manager",
                 "AI Engineer", "Cybersecurity Analyst", "Database Administrator",
                 "QA Engineer", "Network Engineer", "Blockchain Developer",
                 "Game Developer", "System Administrator"]
            )
            
            experience_years = st.slider("Years of Experience", 0, 15, 3)
            
            location_salary = st.selectbox(
                "Work Location",
                ["Bangalore", "Mumbai", "Delhi", "Hyderabad", "Pune",
                 "Chennai", "Kolkata", "Ahmedabad", "Gurgaon", "Noida", "Remote", "India"]
            )
            
            skills_for_salary = st.text_area(
                "Your Skills (comma-separated)",
                value="Python, SQL, ML, Cloud, Docker",
                help="Enter your technical skills"
            )
            
            education_level = st.selectbox(
                "Education Level",
                ["Bachelor", "Master", "PhD"]
            )
        
        with col2:
            st.subheader("Salary Prediction")
            
            if st.button("Predict Salary", type="primary"):
                try:
                    # Load salary predictor
                    salary_predictor = SalaryPredictor()
                    
                    # Train model if not already trained
                    if salary_predictor.model is None:
                        with st.spinner("Training salary prediction model..."):
                            salary_predictor.train()
                    
                    # Parse skills
                    skills_list = [s.strip() for s in skills_for_salary.split(',')]
                    
                    # Predict salary
                    prediction = salary_predictor.predict_salary(
                        career=career_for_salary,
                        experience_years=experience_years,
                        location=location_salary,
                        skills=skills_list,
                        education=education_level
                    )
                    
                    # Display results
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; 
                         border-left: 5px solid #1f77b4;">
                        <h3>Predicted Salary</h3>
                        <h2 style="color: #1f77b4;">₹{prediction['predicted_salary']} LPA</h2>
                        <p><strong>Range:</strong> ₹{prediction['min_salary']} - ₹{prediction['max_salary']} LPA</p>
                        <p><strong>Market Position:</strong> {prediction['market_position']}</p>
                        <p><strong>Confidence:</strong> {prediction['confidence']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Key Factors:**")
                    for key, value in prediction['factors'].items():
                        st.write(f"- **{key.title()}**: {value}")
                    
                    st.write("**Recommendations to Increase Salary:**")
                    for rec in prediction['recommendations']:
                        st.write(f"✓ {rec}")
                
                except Exception as e:
                    st.error(f"Error predicting salary: {e}")
    
    with tab3:
        st.header("📊 Skills Gap Analysis")
        
        st.write("Analyze the gap between your current skills and target career requirements")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Your Information")
            
            target_career = st.selectbox(
                "Target Career",
                ["Data Scientist", "Machine Learning Engineer", "Software Developer",
                 "Full Stack Developer", "Data Analyst", "DevOps Engineer",
                 "Cloud Engineer", "Web Developer", "Mobile Developer",
                 "UI/UX Developer", "Business Analyst", "Product Manager",
                 "AI Engineer", "Cybersecurity Analyst", "Database Administrator",
                 "QA Engineer", "Network Engineer", "Blockchain Developer",
                 "Game Developer", "System Administrator"],
                key="gap_career"
            )
            
            current_skills = st.text_area(
                "Your Current Skills (comma-separated)",
                value="Python, SQL, Excel",
                help="Enter all your technical skills"
            )
        
        with col2:
            st.subheader("Gap Analysis Results")
            
            if st.button("Analyze Skills Gap", type="primary"):
                try:
                    analyzer = SkillsGapAnalyzer()
                    
                    # Parse skills
                    skills_list = [s.strip() for s in current_skills.split(',')]
                    
                    # Analyze gap
                    analysis = analyzer.analyze_skills_gap(skills_list, target_career)
                    
                    # Display readiness
                    st.markdown(f"""
                    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; 
                         border-left: 5px solid #1f77b4;">
                        <h3>Overall Readiness</h3>
                        <h2 style="color: #1f77b4;">{analysis['overall_readiness']}%</h2>
                        <p><strong>{analysis['readiness_level']}</strong></p>
                        <p><strong>Estimated Time:</strong> {analysis['estimated_time_to_readiness']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Skills breakdown
                    st.write("### Skills Breakdown")
                    
                    # Essential skills
                    essential = analysis['skills_analysis']['essential_skills']
                    st.write(f"**Essential Skills Score: {essential['score']}%**")
                    if essential['gaps']:
                        st.write(f"⚠️ **Missing Essential Skills:** {', '.join(essential['gaps'][:5])}")
                    if essential['matched']:
                        st.write(f"✅ **Matched:** {', '.join(essential['matched'][:5])}")
                    
                    # Priority skills to learn
                    st.write("### 🎯 Priority Skills to Learn")
                    for skill in analysis['priority_skills_to_learn']:
                        st.write(f"• **{skill}**")
                    
                    # Next steps
                    st.write("### 📋 Next Steps")
                    for i, step in enumerate(analysis['next_steps'], 1):
                        st.write(f"{i}. {step}")
                    
                    # Certifications
                    if analysis['certifications']:
                        st.write("### 🎓 Recommended Certifications")
                        for cert in analysis['certifications']:
                            st.write(f"• {cert}")
                
                except Exception as e:
                    st.error(f"Error analyzing skills gap: {e}")
    
    with tab4:
        st.header("🗺️ Career Roadmap")
        
        st.write("Get a personalized learning path for your target career")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            roadmap_career = st.selectbox(
                "Select Career Path",
                ["Data Scientist", "Software Developer", "Full Stack Developer",
                 "DevOps Engineer", "Mobile Developer", "Data Analyst"],
                key="roadmap_career"
            )
            
            current_level = st.radio(
                "Your Current Level",
                ["Beginner", "Intermediate", "Advanced"]
            )
            
            if st.button("Generate Roadmap", type="primary"):
                try:
                    generator = CareerRoadmapGenerator()
                    roadmap = generator.generate_roadmap(roadmap_career, current_level)
                    
                    st.session_state.roadmap = roadmap
                
                except Exception as e:
                    st.error(f"Error generating roadmap: {e}")
        
        with col2:
            if 'roadmap' in st.session_state:
                roadmap = st.session_state.roadmap
                
                st.markdown(f"""
                <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px;">
                    <h3>{roadmap['career']}</h3>
                    <p><strong>Total Duration:</strong> {roadmap['total_duration']}</p>
                    <p><strong>Total Steps:</strong> {roadmap['total_steps']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.write("### 🎯 Learning Path")
                
                for i, level in enumerate(roadmap['roadmap'], 1):
                    with st.expander(f"Level {i}: {level['level']} ({level['duration']})"):
                        for j, step in enumerate(level['steps'], 1):
                            st.write(f"**{j}. {step['title']}**")
                            st.write(f"*Skills:* {', '.join(step['skills'])}")
                            st.write(f"*Resources:* {', '.join(step['resources'][:2])}")
                            st.write("---")
                
                st.write("### 🎖️ Milestones")
                for milestone in roadmap['milestones']:
                    st.write(f"✓ {milestone}")
                
                st.write("### 💡 Career Tips")
                for tip in roadmap['tips']:
                    st.write(f"• {tip}")
    
    with tab5:
        st.header("📊 Dataset Analysis")
        
        if df is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Career Distribution")
                career_counts = df['Recommended_Career'].value_counts()
                st.bar_chart(career_counts)
            
            with col2:
                st.subheader("Score Distribution")
                score_data = df[['10th_Score', '12th_Score', 'UG_Score']].mean()
                st.bar_chart(score_data)
            
            st.subheader("Dataset Preview")
            st.dataframe(df.head(10))
            
            st.subheader("Dataset Statistics")
            st.dataframe(df.describe())
    
    with tab5:
        st.header("💼 Job Search")
        
        col1, col2 = st.columns(2)
        
        with col1:
            job_title = st.text_input("Job Title", value="Data Scientist")
            location = st.text_input("Location", value="India")
            max_jobs = st.slider("Number of Jobs", 1, 20, 10)
            use_sample = st.checkbox("Use Sample Data", value=False)
        
        with col2:
            if st.button("Search Jobs", type="primary"):
                try:
                    job_scraper = JobScraper()
                    jobs = job_scraper.scrape_jobs(
                        job_title=job_title,
                        location=location,
                        max_jobs=max_jobs,
                        use_sample=use_sample
                    )
                    
                    if jobs:
                        st.write(f"**Found {len(jobs)} jobs:**")
                        for i, job in enumerate(jobs, 1):
                            with st.expander(f"{i}. {job['title']} - {job['company']}"):
                                st.write(f"**Company:** {job['company']}")
                                st.write(f"**Location:** {job['location']}")
                                st.write(f"**Salary:** {job['salary']}")
                                st.write(f"**Description:** {job['description']}")
                                st.write(f"**Apply:** [Click here]({job['apply_link']})")
                                st.write(f"**Source:** {job['source']}")
                    else:
                        st.warning("No jobs found.")
                
                except Exception as e:
                    st.error(f"Error searching jobs: {e}")
    
    with tab6:
        st.header("📈 Model Information")
        
        if model is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Model Details")
                st.write(f"**Model Type:** {model.model_type}")
                st.write(f"**Features:** {len(model.feature_columns)}")
                st.write(f"**Trained:** ✅")
            
            with col2:
                st.subheader("Top Features")
                feature_importance = model.get_feature_importance(10)
                if feature_importance:
                    feature_df = pd.DataFrame(feature_importance, columns=['Feature', 'Importance'])
                    st.bar_chart(feature_df.set_index('Feature'))
                else:
                    st.write("Feature importance not available.")
            
            st.subheader("Feature List")
            st.write(f"Total features: {len(model.feature_columns)}")
            st.write("First 20 features:")
            st.write(model.feature_columns[:20])

if __name__ == "__main__":
    main()
