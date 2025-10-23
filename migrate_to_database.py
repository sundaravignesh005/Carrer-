"""
Database Migration Script

This script migrates existing CSV data to SQLite database
and initializes the database schema.
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from database import DatabaseManager, migrate_csv_to_database
import logging
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(reset=False):
    """Run database migration."""
    print("="*50)
    print("Career System - Database Migration")
    print("="*50)
    
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Initialize database
    db = DatabaseManager('data/career_system.db')
    
    # Check if database already exists
    if os.path.exists('data/career_system.db') and reset:
        print("\n[1/4] Dropping existing tables...")
        db.drop_all_tables()
    elif os.path.exists('data/career_system.db'):
        print("\n[1/4] Keeping existing database. Will only create missing tables.")
    else:
        print("\n[1/4] Creating new database...")
    # Create tables
    print("\n[2/4] Creating database tables...")
    db.create_tables()
    print("[OK] All tables created successfully")
    
    # Migrate CSV data
    csv_path = 'data/career_data.csv'
    if os.path.exists(csv_path):
        print(f"\n[3/4] Migrating data from {csv_path}...")
        try:
            migrate_csv_to_database(csv_path, db)
            print("[OK] Data migration completed")
        except Exception as e:
            print(f"[ERROR] Error migrating data: {e}")
    else:
        print(f"\n[3/4] No CSV file found at {csv_path}, skipping data migration")
    
    # Get statistics
    print("\n[4/4] Database Statistics:")
    analytics = db.get_analytics()
    print(f"  - Total Users: {analytics['total_users']}")
    print(f"  - Total Career Records: {len(db.get_all_career_data())}")
    print(f"  - Total Predictions: {analytics['total_predictions']}")
    print(f"  - Total Jobs: {analytics['total_jobs']}")
    
    print("\n" + "="*50)
    print("[OK] Migration completed successfully!")
    print("="*50)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Migrate career system to database')
    parser.add_argument('--reset', action='store_true', help='Reset existing database')
    args = parser.parse_args()
    
    main(reset=args.reset)

