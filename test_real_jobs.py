"""
Test Real Job Scraping

This script tests the real job scraping functionality from LinkedIn, Indeed, and Naukri.
"""

import sys
import os

# Add src directory to path
sys.path.append('src')

from jobs_scraper import JobScraper

def test_real_job_scraping():
    """Test real job scraping from multiple sources."""
    
    print("🔍 Testing Real Job Scraping from LinkedIn, Indeed, and Naukri")
    print("=" * 70)
    
    # Initialize job scraper
    scraper = JobScraper()
    
    # Test job search
    job_title = "Data Scientist"
    location = "India"
    max_jobs = 5
    
    print(f"Searching for: {job_title} in {location}")
    print(f"Max jobs: {max_jobs}")
    print("-" * 50)
    
    try:
        # Scrape real jobs
        jobs = scraper.scrape_jobs(
            job_title=job_title,
            location=location,
            max_jobs=max_jobs,
            use_sample=False  # Use real scraping
        )
        
        if jobs:
            print(f"✅ Found {len(jobs)} real job openings!")
            print("\n📋 Job Listings:")
            
            for i, job in enumerate(jobs, 1):
                print(f"\n{i}. {job['title']}")
                print(f"   🏢 Company: {job['company']}")
                print(f"   📍 Location: {job['location']}")
                print(f"   💰 Salary: {job['salary']}")
                print(f"   🔗 Apply: {job['apply_link']}")
                print(f"   🌐 Source: {job['source']}")
                print(f"   📝 Description: {job['description'][:100]}...")
        else:
            print("❌ No jobs found. This might be due to:")
            print("   - Network connectivity issues")
            print("   - Website structure changes")
            print("   - Rate limiting")
            print("   - The system will fall back to sample data")
            
    except Exception as e:
        print(f"❌ Error during job scraping: {e}")
        print("The system will fall back to sample data for demonstration")

if __name__ == "__main__":
    test_real_job_scraping()
