#!/usr/bin/env python3
"""
Database Viewer Script
View data from the Career Recommendation System database
"""

import sys
import os
sys.path.append('src')

from database import DatabaseManager
import pandas as pd

def main():
    print("="*60)
    print("CAREER RECOMMENDATION SYSTEM - DATABASE VIEWER")
    print("="*60)
    
    # Initialize database
    db = DatabaseManager('data/career_system.db')
    
    # 1. View Career Data
    print("\n[1] CAREER TRAINING DATA")
    print("-" * 40)
    career_data = db.get_all_career_data()
    if career_data:
        df_careers = pd.DataFrame(career_data)
        print(f"Total Records: {len(df_careers)}")
        print("\nFirst 5 records:")
        print(df_careers[['score_10th', 'score_12th', 'score_ug', 'skills', 'recommended_career']].head())
        
        # Show career distribution
        print(f"\nCareer Distribution:")
        career_counts = df_careers['recommended_career'].value_counts()
        for career, count in career_counts.head(10).items():
            print(f"  {career}: {count} records")
    else:
        print("No career data found")
    
    # 2. View Jobs Data
    print("\n\n[2] JOB POSTINGS")
    print("-" * 40)
    jobs = db.search_jobs(limit=10)
    if jobs:
        df_jobs = pd.DataFrame(jobs)
        print(f"Total Jobs: {len(df_jobs)}")
        print("\nRecent job postings:")
        for job in jobs[:5]:
            print(f"  • {job['title']} at {job['company']} ({job['location']})")
    else:
        print("No jobs found")
    
    # 3. View System Analytics
    print("\n\n[3] SYSTEM ANALYTICS")
    print("-" * 40)
    analytics = db.get_analytics()
    for key, value in analytics.items():
        if key == 'top_careers':
            print(f"{key}:")
            for career in value[:5]:
                print(f"  • {career['predicted_career']}: {career['count']} predictions")
        else:
            print(f"{key}: {value}")
    
    # 4. View Database Tables
    print("\n\n[4] DATABASE TABLES")
    print("-" * 40)
    import sqlite3
    conn = sqlite3.connect('data/career_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print("Available tables:")
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  • {table_name}: {count} records")
    conn.close()
    
    print("\n" + "="*60)
    print("[OK] Database viewing completed!")
    print("="*60)

if __name__ == "__main__":
    main()
