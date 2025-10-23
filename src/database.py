"""
Database Module for Career Recommendation System

This module handles all database operations using SQLite.
Includes tables for users, career data, jobs, feedback, and predictions.
"""

import sqlite3
import os
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import json
import hashlib
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Handles all database operations for the career recommendation system.
    """
    
    def __init__(self, db_path: str = 'data/career_system.db'):
        """
        Initialize the database manager.
        
        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.ensure_database_exists()
    
    def ensure_database_exists(self):
        """Create database directory if it doesn't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """
        Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def create_tables(self):
        """Create all database tables."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    is_admin BOOLEAN DEFAULT 0
                )
            """)
            
            # Career training data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS career_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT,
                    score_10th REAL NOT NULL,
                    score_12th REAL NOT NULL,
                    score_ug REAL NOT NULL,
                    skills TEXT NOT NULL,
                    interests TEXT NOT NULL,
                    recommended_career TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    score_10th REAL,
                    score_12th REAL,
                    score_ug REAL,
                    pg_score REAL,
                    skills TEXT,
                    interests TEXT,
                    location TEXT,
                    resume_path TEXT,
                    linkedin_url TEXT,
                    github_url TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Predictions history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    prediction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    predicted_career TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    top_predictions TEXT,
                    input_data TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                )
            """)
            
            # Jobs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    location TEXT,
                    salary TEXT,
                    description TEXT,
                    apply_link TEXT,
                    source TEXT,
                    career_category TEXT,
                    skills_required TEXT,
                    experience_required TEXT,
                    posted_date TIMESTAMP,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            """)
            
            # Saved jobs table (bookmarks)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS saved_jobs (
                    saved_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (job_id) REFERENCES jobs (job_id),
                    UNIQUE(user_id, job_id)
                )
            """)
            
            # Job applications tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_applications (
                    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    job_id INTEGER NOT NULL,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'applied',
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (job_id) REFERENCES jobs (job_id)
                )
            """)
            
            # Feedback table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    prediction_id INTEGER,
                    job_id INTEGER,
                    rating INTEGER CHECK(rating >= 1 AND rating <= 5),
                    comments TEXT,
                    feedback_type TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (prediction_id) REFERENCES predictions (prediction_id),
                    FOREIGN KEY (job_id) REFERENCES jobs (job_id)
                )
            """)
            
            # Model metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS model_metrics (
                    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model_type TEXT NOT NULL,
                    accuracy REAL,
                    cv_mean REAL,
                    cv_std REAL,
                    training_samples INTEGER,
                    feature_count INTEGER,
                    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT
                )
            """)
            
            # Skills catalog table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills_catalog (
                    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_name TEXT UNIQUE NOT NULL,
                    category TEXT,
                    demand_score REAL,
                    average_salary REAL,
                    trending BOOLEAN DEFAULT 0,
                    learning_resources TEXT
                )
            """)
            
            # Career roadmaps table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS career_roadmaps (
                    roadmap_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    career_name TEXT NOT NULL,
                    level TEXT NOT NULL,
                    step_number INTEGER NOT NULL,
                    step_title TEXT NOT NULL,
                    step_description TEXT,
                    skills_needed TEXT,
                    estimated_duration TEXT,
                    resources TEXT
                )
            """)
            
            # Salary data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS salary_data (
                    salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    career TEXT NOT NULL,
                    location TEXT,
                    experience_years INTEGER,
                    skills TEXT,
                    min_salary REAL,
                    max_salary REAL,
                    average_salary REAL,
                    currency TEXT DEFAULT 'INR',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            logger.info("All database tables created successfully")
    
    def drop_all_tables(self):
        """Drop all tables (for testing/reset purposes)."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            tables = [
                'users', 'career_data', 'user_profiles', 'predictions',
                'jobs', 'saved_jobs', 'job_applications', 'feedback',
                'model_metrics', 'skills_catalog', 'career_roadmaps', 'salary_data'
            ]
            
            for table in tables:
                cursor.execute(f"DROP TABLE IF EXISTS {table}")
            
            logger.info("All tables dropped successfully")
    
    # ==================== USER OPERATIONS ====================
    
    def create_user(self, email: str, password: str, full_name: str) -> int:
        """
        Create a new user.
        
        Args:
            email (str): User email
            password (str): User password (will be hashed)
            full_name (str): User's full name
            
        Returns:
            int: User ID
        """
        password_hash = self._hash_password(password)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (email, password_hash, full_name)
                VALUES (?, ?, ?)
            """, (email, password_hash, full_name))
            
            user_id = cursor.lastrowid
            logger.info(f"User created: {email} (ID: {user_id})")
            return user_id
    
    def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate a user.
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            Optional[Dict[str, Any]]: User data if authenticated, None otherwise
        """
        password_hash = self._hash_password(password)
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, email, full_name, is_admin
                FROM users
                WHERE email = ? AND password_hash = ? AND is_active = 1
            """, (email, password_hash))
            
            row = cursor.fetchone()
            if row:
                # Update last login
                cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (row['user_id'],))
                
                return dict(row)
            return None
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user by ID."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT user_id, email, full_name, created_at, last_login, is_admin
                FROM users
                WHERE user_id = ?
            """, (user_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    # ==================== CAREER DATA OPERATIONS ====================
    
    def insert_career_data(self, data: Dict[str, Any]) -> int:
        """
        Insert career training data.
        
        Args:
            data (Dict[str, Any]): Career data dictionary
            
        Returns:
            int: Record ID
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO career_data 
                (student_id, score_10th, score_12th, score_ug, skills, interests, recommended_career)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('student_id'),
                data['score_10th'],
                data['score_12th'],
                data['score_ug'],
                data['skills'],
                data['interests'],
                data['recommended_career']
            ))
            
            return cursor.lastrowid
    
    def get_all_career_data(self) -> List[Dict[str, Any]]:
        """Get all career training data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, student_id, score_10th, score_12th, score_ug, 
                       skills, interests, recommended_career, created_at
                FROM career_data
            """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    def bulk_insert_career_data(self, data_list: List[Dict[str, Any]]):
        """Bulk insert career data."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT INTO career_data 
                (student_id, score_10th, score_12th, score_ug, skills, interests, recommended_career)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    d.get('student_id'),
                    d['score_10th'],
                    d['score_12th'],
                    d['score_ug'],
                    d['skills'],
                    d['interests'],
                    d['recommended_career']
                )
                for d in data_list
            ])
            
            logger.info(f"Bulk inserted {len(data_list)} career records")
    
    # ==================== PREDICTION OPERATIONS ====================
    
    def save_prediction(self, user_id: Optional[int], prediction_data: Dict[str, Any]) -> int:
        """Save a career prediction."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO predictions 
                (user_id, predicted_career, confidence_score, top_predictions, 
                 input_data, model_used)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                prediction_data['career'],
                prediction_data['confidence'],
                json.dumps(prediction_data.get('top_predictions', [])),
                json.dumps(prediction_data.get('input_data', {})),
                prediction_data.get('model_used', 'random_forest')
            ))
            
            return cursor.lastrowid
    
    def get_user_predictions(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's prediction history."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT prediction_id, predicted_career, confidence_score, 
                       top_predictions, created_at
                FROM predictions
                WHERE user_id = ?
                ORDER BY created_at DESC
                LIMIT ?
            """, (user_id, limit))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                result['top_predictions'] = json.loads(result['top_predictions'])
                results.append(result)
            
            return results
    
    # ==================== JOB OPERATIONS ====================
    
    def insert_job(self, job_data: Dict[str, Any]) -> int:
        """Insert a job posting."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO jobs 
                (title, company, location, salary, description, apply_link, 
                 source, career_category, skills_required)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                job_data['title'],
                job_data['company'],
                job_data.get('location', ''),
                job_data.get('salary', ''),
                job_data.get('description', ''),
                job_data.get('apply_link', ''),
                job_data.get('source', ''),
                job_data.get('career_category', ''),
                job_data.get('skills_required', '')
            ))
            
            return cursor.lastrowid
    
    def bulk_insert_jobs(self, jobs: List[Dict[str, Any]]):
        """Bulk insert job postings."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany("""
                INSERT INTO jobs 
                (title, company, location, salary, description, apply_link, 
                 source, career_category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, [
                (
                    job['title'],
                    job['company'],
                    job.get('location', ''),
                    job.get('salary', ''),
                    job.get('description', ''),
                    job.get('apply_link', ''),
                    job.get('source', ''),
                    job.get('career_category', '')
                )
                for job in jobs
            ])
            
            logger.info(f"Bulk inserted {len(jobs)} job postings")
    
    def search_jobs(self, career: str = None, location: str = None, 
                    limit: int = 20) -> List[Dict[str, Any]]:
        """Search for jobs."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            query = "SELECT * FROM jobs WHERE is_active = 1"
            params = []
            
            if career:
                query += " AND (title LIKE ? OR career_category LIKE ?)"
                params.extend([f"%{career}%", f"%{career}%"])
            
            if location:
                query += " AND location LIKE ?"
                params.append(f"%{location}%")
            
            query += " ORDER BY scraped_at DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def save_job_for_user(self, user_id: int, job_id: int, notes: str = None) -> int:
        """Save/bookmark a job for user."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO saved_jobs (user_id, job_id, notes)
                VALUES (?, ?, ?)
            """, (user_id, job_id, notes))
            
            return cursor.lastrowid
    
    def track_application(self, user_id: int, job_id: int, notes: str = None) -> int:
        """Track a job application."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO job_applications (user_id, job_id, notes)
                VALUES (?, ?, ?)
            """, (user_id, job_id, notes))
            
            return cursor.lastrowid
    
    # ==================== FEEDBACK OPERATIONS ====================
    
    def save_feedback(self, feedback_data: Dict[str, Any]) -> int:
        """Save user feedback."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO feedback 
                (user_id, prediction_id, job_id, rating, comments, feedback_type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                feedback_data.get('user_id'),
                feedback_data.get('prediction_id'),
                feedback_data.get('job_id'),
                feedback_data['rating'],
                feedback_data.get('comments', ''),
                feedback_data.get('feedback_type', 'general')
            ))
            
            return cursor.lastrowid
    
    def get_all_feedback(self) -> List[Dict[str, Any]]:
        """Get all feedback."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM feedback
                ORDER BY created_at DESC
            """)
            
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== ANALYTICS ====================
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get system analytics."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) as count FROM users")
            total_users = cursor.fetchone()['count']
            
            # Total predictions
            cursor.execute("SELECT COUNT(*) as count FROM predictions")
            total_predictions = cursor.fetchone()['count']
            
            # Total jobs
            cursor.execute("SELECT COUNT(*) as count FROM jobs WHERE is_active = 1")
            total_jobs = cursor.fetchone()['count']
            
            # Average rating
            cursor.execute("SELECT AVG(rating) as avg_rating FROM feedback")
            avg_rating = cursor.fetchone()['avg_rating'] or 0
            
            # Top careers
            cursor.execute("""
                SELECT predicted_career, COUNT(*) as count
                FROM predictions
                GROUP BY predicted_career
                ORDER BY count DESC
                LIMIT 10
            """)
            top_careers = [dict(row) for row in cursor.fetchall()]
            
            return {
                'total_users': total_users,
                'total_predictions': total_predictions,
                'total_jobs': total_jobs,
                'average_rating': round(avg_rating, 2),
                'top_careers': top_careers
            }


def migrate_csv_to_database(csv_path: str, db: DatabaseManager):
    """
    Migrate career data from CSV to database.
    
    Args:
        csv_path (str): Path to CSV file
        db (DatabaseManager): Database manager instance
    """
    import pandas as pd
    
    try:
        df = pd.read_csv(csv_path)
        
        data_list = []
        for _, row in df.iterrows():
            data_list.append({
                'student_id': str(row.get('Student_ID', '')),
                'score_10th': float(row['10th_Score']),
                'score_12th': float(row['12th_Score']),
                'score_ug': float(row['UG_Score']),
                'skills': str(row['Skills']),
                'interests': str(row['Interests']),
                'recommended_career': str(row['Recommended_Career'])
            })
        
        db.bulk_insert_career_data(data_list)
        logger.info(f"Successfully migrated {len(data_list)} records from CSV to database")
        
    except Exception as e:
        logger.error(f"Error migrating CSV to database: {e}")
        raise


def main():
    """Test database operations."""
    # Initialize database
    db = DatabaseManager('data/career_system.db')
    
    # Create tables
    db.create_tables()
    
    # Test user creation
    try:
        user_id = db.create_user('test@example.com', 'password123', 'Test User')
        print(f"Created user with ID: {user_id}")
        
        # Test authentication
        user = db.authenticate_user('test@example.com', 'password123')
        print(f"Authenticated user: {user}")
        
        # Migrate CSV data
        if os.path.exists('data/career_data.csv'):
            migrate_csv_to_database('data/career_data.csv', db)
        
        # Get analytics
        analytics = db.get_analytics()
        print(f"\nSystem Analytics: {json.dumps(analytics, indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

