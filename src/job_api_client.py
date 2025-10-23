"""
Job API Client Module

This module integrates with real job APIs (RapidAPI, Adzuna, RemoteOK)
to fetch live job postings.
"""

import requests
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JobAPIClient:
    """
    Client for fetching jobs from various job APIs.
    """
    
    def __init__(self):
        """Initialize the job API client."""
        # API keys from environment variables
        self.rapidapi_key = os.getenv('RAPIDAPI_KEY', '')
        self.adzuna_app_id = os.getenv('ADZUNA_APP_ID', '')
        self.adzuna_app_key = os.getenv('ADZUNA_APP_KEY', '')
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_from_rapidapi_jsearch(self, job_title: str, location: str = "India", 
                                    max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch jobs from RapidAPI JSearch API.
        
        Args:
            job_title (str): Job title to search
            location (str): Location
            max_results (int): Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        if not self.rapidapi_key:
            logger.warning("RapidAPI key not set. Skipping RapidAPI.")
            return []
        
        try:
            url = "https://jsearch.p.rapidapi.com/search"
            
            headers = {
                "X-RapidAPI-Key": self.rapidapi_key,
                "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
            }
            
            params = {
                "query": f"{job_title} in {location}",
                "page": "1",
                "num_pages": "1",
                "date_posted": "all"
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = []
            
            for job in data.get('data', [])[:max_results]:
                jobs.append({
                    'title': job.get('job_title', 'N/A'),
                    'company': job.get('employer_name', 'N/A'),
                    'location': job.get('job_city', location) or location,
                    'salary': self._format_salary(job.get('job_min_salary'), job.get('job_max_salary')),
                    'description': job.get('job_description', 'No description available')[:500],
                    'apply_link': job.get('job_apply_link', '#'),
                    'source': 'RapidAPI JSearch',
                    'posted_date': job.get('job_posted_at_datetime_utc', ''),
                    'employment_type': job.get('job_employment_type', 'Full-time')
                })
            
            logger.info(f"Fetched {len(jobs)} jobs from RapidAPI JSearch")
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching from RapidAPI: {e}")
            return []
    
    def fetch_from_adzuna(self, job_title: str, location: str = "India", 
                         max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch jobs from Adzuna API.
        
        Args:
            job_title (str): Job title to search
            location (str): Location
            max_results (int): Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        if not self.adzuna_app_id or not self.adzuna_app_key:
            logger.warning("Adzuna API credentials not set. Skipping Adzuna.")
            return []
        
        try:
            # Adzuna country codes
            country_code = 'in'  # India
            
            url = f"https://api.adzuna.com/v1/api/jobs/{country_code}/search/1"
            
            params = {
                'app_id': self.adzuna_app_id,
                'app_key': self.adzuna_app_key,
                'results_per_page': max_results,
                'what': job_title,
                'where': location,
                'content-type': 'application/json'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = []
            
            for job in data.get('results', []):
                jobs.append({
                    'title': job.get('title', 'N/A'),
                    'company': job.get('company', {}).get('display_name', 'N/A'),
                    'location': job.get('location', {}).get('display_name', location),
                    'salary': self._format_salary_range(job.get('salary_min'), job.get('salary_max')),
                    'description': job.get('description', 'No description available')[:500],
                    'apply_link': job.get('redirect_url', '#'),
                    'source': 'Adzuna',
                    'posted_date': job.get('created', ''),
                    'contract_type': job.get('contract_type', 'permanent')
                })
            
            logger.info(f"Fetched {len(jobs)} jobs from Adzuna")
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching from Adzuna: {e}")
            return []
    
    def fetch_from_remoteok(self, job_title: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch remote jobs from RemoteOK API.
        
        Args:
            job_title (str): Job title to search
            max_results (int): Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        try:
            url = "https://remoteok.com/api"
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            jobs = []
            
            # Filter jobs by title
            job_title_lower = job_title.lower()
            
            for job in data[1:]:  # Skip first item (metadata)
                if len(jobs) >= max_results:
                    break
                
                title = job.get('position', '').lower()
                if job_title_lower in title or any(keyword in title for keyword in job_title_lower.split()):
                    jobs.append({
                        'title': job.get('position', 'N/A'),
                        'company': job.get('company', 'N/A'),
                        'location': job.get('location', 'Remote'),
                        'salary': f"${job.get('salary_min', 0)}-${job.get('salary_max', 0)}" if job.get('salary_min') else 'Not specified',
                        'description': job.get('description', 'No description available')[:500],
                        'apply_link': job.get('url', '#'),
                        'source': 'RemoteOK',
                        'posted_date': job.get('date', ''),
                        'tags': ','.join(job.get('tags', []))
                    })
            
            logger.info(f"Fetched {len(jobs)} jobs from RemoteOK")
            return jobs
            
        except Exception as e:
            logger.error(f"Error fetching from RemoteOK: {e}")
            return []
    
    def fetch_from_github_jobs(self, job_title: str, location: str = "", 
                              max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Fetch jobs from GitHub Jobs API (archived, but keeping for reference).
        Note: GitHub Jobs API was discontinued in May 2021.
        This is a placeholder for demonstration.
        
        Args:
            job_title (str): Job title to search
            location (str): Location
            max_results (int): Maximum number of results
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        logger.info("GitHub Jobs API is no longer available")
        return []
    
    def fetch_all_sources(self, job_title: str, location: str = "India", 
                         max_results_per_source: int = 5) -> List[Dict[str, Any]]:
        """
        Fetch jobs from all available sources.
        
        Args:
            job_title (str): Job title to search
            location (str): Location
            max_results_per_source (int): Max results per source
            
        Returns:
            List[Dict[str, Any]]: Combined list of job postings
        """
        all_jobs = []
        
        # Try RapidAPI
        rapidapi_jobs = self.fetch_from_rapidapi_jsearch(job_title, location, max_results_per_source)
        all_jobs.extend(rapidapi_jobs)
        
        # Try Adzuna
        adzuna_jobs = self.fetch_from_adzuna(job_title, location, max_results_per_source)
        all_jobs.extend(adzuna_jobs)
        
        # Try RemoteOK (for remote positions)
        remoteok_jobs = self.fetch_from_remoteok(job_title, max_results_per_source)
        all_jobs.extend(remoteok_jobs)
        
        # Remove duplicates based on title and company
        unique_jobs = self._remove_duplicates(all_jobs)
        
        logger.info(f"Total unique jobs fetched: {len(unique_jobs)} from {len(set(j['source'] for j in unique_jobs))} sources")
        
        return unique_jobs
    
    def _format_salary(self, min_sal: Optional[float], max_sal: Optional[float]) -> str:
        """Format salary range."""
        if min_sal and max_sal:
            return f"${min_sal:,.0f}-${max_sal:,.0f}"
        elif min_sal:
            return f"${min_sal:,.0f}+"
        elif max_sal:
            return f"Up to ${max_sal:,.0f}"
        return "Not specified"
    
    def _format_salary_range(self, min_sal: Optional[float], max_sal: Optional[float]) -> str:
        """Format salary range for INR."""
        if min_sal and max_sal:
            return f"₹{min_sal:,.0f}-₹{max_sal:,.0f}"
        elif min_sal:
            return f"₹{min_sal:,.0f}+"
        elif max_sal:
            return f"Up to ₹{max_sal:,.0f}"
        return "Not specified"
    
    def _remove_duplicates(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate jobs based on title and company."""
        seen = set()
        unique_jobs = []
        
        for job in jobs:
            key = (job['title'].lower(), job['company'].lower())
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        return unique_jobs
    
    def save_api_keys(self, rapidapi_key: str = None, adzuna_app_id: str = None, 
                     adzuna_app_key: str = None):
        """
        Save API keys to environment file.
        
        Args:
            rapidapi_key (str): RapidAPI key
            adzuna_app_id (str): Adzuna App ID
            adzuna_app_key (str): Adzuna App Key
        """
        env_file = '.env'
        env_vars = {}
        
        # Read existing .env file
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value
        
        # Update with new keys
        if rapidapi_key:
            env_vars['RAPIDAPI_KEY'] = rapidapi_key
            self.rapidapi_key = rapidapi_key
        
        if adzuna_app_id:
            env_vars['ADZUNA_APP_ID'] = adzuna_app_id
            self.adzuna_app_id = adzuna_app_id
        
        if adzuna_app_key:
            env_vars['ADZUNA_APP_KEY'] = adzuna_app_key
            self.adzuna_app_key = adzuna_app_key
        
        # Write back to .env file
        with open(env_file, 'w') as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")
        
        logger.info("API keys saved to .env file")


def main():
    """Test job API client."""
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    client = JobAPIClient()
    
    print("Testing Job API Client")
    print("="*60)
    
    # Test RemoteOK (no API key required)
    print("\n1. Testing RemoteOK API:")
    jobs = client.fetch_from_remoteok("Data Scientist", max_results=3)
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Source: {job['source']}")
    
    # Test fetching from all sources
    print("\n\n2. Testing All Sources:")
    all_jobs = client.fetch_all_sources("Software Developer", "India", max_results_per_source=2)
    print(f"\nTotal jobs found: {len(all_jobs)}")
    for i, job in enumerate(all_jobs, 1):
        print(f"\n{i}. {job['title']} - {job['company']}")
        print(f"   Source: {job['source']}")


if __name__ == "__main__":
    main()

