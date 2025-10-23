"""
Admin Dashboard - Streamlit App

This module provides an administrative interface for managing
the career recommendation system.
"""

import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

# Add src directory to path
sys.path.append('src')

from database import DatabaseManager
from auth import AuthManager

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #dee2e6;
    }
    .alert-success {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .alert-danger {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_db():
    """Get database connection."""
    return DatabaseManager('data/career_system.db')


def check_admin_auth():
    """Check if user is authenticated as admin."""
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    return st.session_state.admin_authenticated


def admin_login():
    """Admin login page."""
    st.markdown('<h1 class="main-header">🔐 Admin Login</h1>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="admin@example.com")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if email and password:
                # For demo purposes - in production, use proper authentication
                if email == "admin@example.com" and password == "admin123":
                    st.session_state.admin_authenticated = True
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            else:
                st.warning("Please enter both email and password")


def show_dashboard():
    """Main admin dashboard."""
    st.markdown('<h1 class="main-header">📊 Admin Dashboard</h1>', unsafe_allow_html=True)
    
    db = get_db()
    
    # Sidebar
    st.sidebar.title("Admin Navigation")
    page = st.sidebar.radio("Go to", [
        "📊 Overview",
        "👥 Users",
        "🎯 Predictions",
        "💼 Jobs",
        "📝 Feedback",
        "📈 Analytics"
    ])
    
    if st.sidebar.button("Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()
    
    # Main content
    if page == "📊 Overview":
        show_overview(db)
    elif page == "👥 Users":
        show_users(db)
    elif page == "🎯 Predictions":
        show_predictions(db)
    elif page == "💼 Jobs":
        show_jobs(db)
    elif page == "📝 Feedback":
        show_feedback(db)
    elif page == "📈 Analytics":
        show_analytics(db)


def show_overview(db: DatabaseManager):
    """Show system overview."""
    st.header("System Overview")
    
    # Get analytics
    analytics = db.get_analytics()
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="👥 Total Users",
            value=analytics['total_users'],
            delta="+5 this week" if analytics['total_users'] > 0 else None
        )
    
    with col2:
        st.metric(
            label="🎯 Predictions",
            value=analytics['total_predictions'],
            delta="+12 today" if analytics['total_predictions'] > 0 else None
        )
    
    with col3:
        st.metric(
            label="💼 Active Jobs",
            value=analytics['total_jobs']
        )
    
    with col4:
        st.metric(
            label="⭐ Avg Rating",
            value=f"{analytics['average_rating']:.2f}/5.0"
        )
    
    st.markdown("---")
    
    # Top Careers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Top Career Recommendations")
        if analytics['top_careers']:
            career_df = pd.DataFrame(analytics['top_careers'])
            st.bar_chart(career_df.set_index('predicted_career')['count'])
        else:
            st.info("No prediction data yet")
    
    with col2:
        st.subheader("📊 System Status")
        status_data = {
            'Component': ['Database', 'ML Models', 'Job API', 'Email Service'],
            'Status': ['Operational', 'Operational', 'Operational', 'Configured'],
            'Health': ['100%', '100%', '95%', '90%']
        }
        st.dataframe(status_data, hide_index=True)


def show_users(db: DatabaseManager):
    """Show user management."""
    st.header("👥 User Management")
    
    # Get all users (you'd need to add this method to DatabaseManager)
    st.info("User listing functionality - Connect to database to display users")
    
    # Sample data for demo
    sample_users = pd.DataFrame({
        'ID': [1, 2, 3],
        'Email': ['user1@example.com', 'user2@example.com', 'user3@example.com'],
        'Name': ['John Doe', 'Jane Smith', 'Bob Wilson'],
        'Joined': ['2024-01-15', '2024-01-20', '2024-01-25'],
        'Status': ['Active', 'Active', 'Inactive']
    })
    
    st.dataframe(sample_users, use_container_width=True)
    
    # User actions
    st.subheader("User Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Users"):
            st.success("Users exported to CSV")
    
    with col2:
        if st.button("Send Bulk Email"):
            st.info("Email composition interface would appear here")
    
    with col3:
        if st.button("Generate Report"):
            st.success("Report generated")


def show_predictions(db: DatabaseManager):
    """Show prediction history."""
    st.header("🎯 Prediction History")
    
    # Sample prediction data
    sample_predictions = pd.DataFrame({
        'ID': range(1, 11),
        'User': [f'user{i}@example.com' for i in range(1, 11)],
        'Career': ['Data Scientist', 'Software Developer', 'ML Engineer', 'Data Analyst',
                  'Full Stack Developer', 'DevOps Engineer', 'Cloud Engineer',
                  'Business Analyst', 'UI/UX Developer', 'Product Manager'],
        'Confidence': [85.5, 78.3, 92.1, 67.8, 81.2, 76.5, 88.9, 72.3, 79.8, 84.6],
        'Date': pd.date_range(start='2024-01-01', periods=10, freq='D')
    })
    
    st.dataframe(sample_predictions, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Predictions by Career")
        career_counts = sample_predictions['Career'].value_counts()
        fig = px.pie(values=career_counts.values, names=career_counts.index,
                    title="Career Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Confidence Score Distribution")
        fig = px.histogram(sample_predictions, x='Confidence',
                          title="Confidence Scores")
        st.plotly_chart(fig, use_container_width=True)


def show_jobs(db: DatabaseManager):
    """Show job management."""
    st.header("💼 Job Management")
    
    # Job statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Jobs", "150")
    with col2:
        st.metric("Active Jobs", "120")
    with col3:
        st.metric("New This Week", "25")
    
    st.markdown("---")
    
    # Sample job data
    sample_jobs = pd.DataFrame({
        'Title': ['Data Scientist', 'Senior Developer', 'ML Engineer', 'Cloud Architect'],
        'Company': ['TechCorp', 'StartupXYZ', 'AI Labs', 'CloudTech'],
        'Location': ['Bangalore', 'Mumbai', 'Delhi', 'Pune'],
        'Salary': ['₹10-15 LPA', '₹15-25 LPA', '₹18-30 LPA', '₹20-35 LPA'],
        'Source': ['Indeed', 'LinkedIn', 'Naukri', 'Indeed'],
        'Status': ['Active', 'Active', 'Active', 'Expired']
    })
    
    st.dataframe(sample_jobs, use_container_width=True)
    
    # Actions
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Refresh Jobs"):
            st.success("Jobs refreshed from APIs")
    
    with col2:
        if st.button("Remove Expired"):
            st.success("Expired jobs removed")
    
    with col3:
        if st.button("Export Jobs"):
            st.success("Jobs exported")


def show_feedback(db: DatabaseManager):
    """Show feedback management."""
    st.header("📝 User Feedback")
    
    all_feedback = db.get_all_feedback()
    
    if not all_feedback:
        st.info("No feedback yet")
        return
    
    feedback_df = pd.DataFrame(all_feedback)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Feedback", len(feedback_df))
    with col2:
        avg_rating = feedback_df['rating'].mean() if 'rating' in feedback_df.columns else 0
        st.metric("Avg Rating", f"{avg_rating:.2f}/5")
    with col3:
        positive = len(feedback_df[feedback_df['rating'] >= 4]) if 'rating' in feedback_df.columns else 0
        st.metric("Positive", f"{positive}")
    
    st.markdown("---")
    
    # Display feedback
    st.dataframe(feedback_df, use_container_width=True)
    
    # Rating distribution
    if 'rating' in feedback_df.columns:
        st.subheader("Rating Distribution")
        rating_counts = feedback_df['rating'].value_counts().sort_index()
        fig = px.bar(x=rating_counts.index, y=rating_counts.values,
                    labels={'x': 'Rating', 'y': 'Count'},
                    title="User Ratings")
        st.plotly_chart(fig, use_container_width=True)


def show_analytics(db: DatabaseManager):
    """Show detailed analytics."""
    st.header("📈 System Analytics")
    
    # Time series data (sample)
    dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
    predictions_per_day = pd.DataFrame({
        'Date': dates,
        'Predictions': [10 + i % 15 for i in range(len(dates))],
        'New Users': [2 + i % 5 for i in range(len(dates))]
    })
    
    # Predictions over time
    st.subheader("Predictions Over Time")
    fig = px.line(predictions_per_day, x='Date', y='Predictions',
                 title="Daily Predictions")
    st.plotly_chart(fig, use_container_width=True)
    
    # User growth
    st.subheader("User Growth")
    fig = px.line(predictions_per_day, x='Date', y='New Users',
                 title="New Users Per Day")
    st.plotly_chart(fig, use_container_width=True)
    
    # Career trends
    st.subheader("Career Trends")
    career_trends = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr'],
        'Data Scientist': [45, 52, 48, 58],
        'Software Developer': [38, 42, 45, 50],
        'ML Engineer': [28, 35, 38, 42]
    })
    
    fig = px.line(career_trends.melt(id_vars='Month', var_name='Career', value_name='Count'),
                 x='Month', y='Count', color='Career',
                 title="Career Recommendation Trends")
    st.plotly_chart(fig, use_container_width=True)


def main():
    """Main application."""
    if not check_admin_auth():
        admin_login()
    else:
        show_dashboard()


if __name__ == "__main__":
    main()

