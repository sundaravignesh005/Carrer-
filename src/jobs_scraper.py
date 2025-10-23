"""
Job Scraping Module for Career Recommendation System

This module handles fetching live job postings from various job portals.
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import random
import logging
from typing import List, Dict, Any, Optional
import re
from urllib.parse import urlencode, quote_plus
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobScraper:
    """
    Handles job scraping from various job portals.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.job_data_path = 'data/sample_jobs.json'
        
        # Sample job data as fallback
        self.sample_jobs = [
            {
                "title": "Data Scientist",
                "company": "TechCorp India",
                "location": "Bangalore, India",
                "salary": "₹8-15 LPA",
                "description": "Looking for a Data Scientist with Python, ML, and SQL skills.",
                "apply_link": "https://example.com/apply/1",
                "source": "Sample Data"
            },
            {
                "title": "Machine Learning Engineer",
                "company": "AI Solutions Pvt Ltd",
                "location": "Mumbai, India",
                "salary": "₹10-18 LPA",
                "description": "ML Engineer position requiring Python, TensorFlow, and cloud experience.",
                "apply_link": "https://example.com/apply/2",
                "source": "Sample Data"
            },
            {
                "title": "Software Developer",
                "company": "DevTech Solutions",
                "location": "Delhi, India",
                "salary": "₹6-12 LPA",
                "description": "Full-stack developer with Java, Spring Boot, and React skills.",
                "apply_link": "https://example.com/apply/3",
                "source": "Sample Data"
            },
            {
                "title": "Business Analyst",
                "company": "Business Intelligence Corp",
                "location": "Pune, India",
                "salary": "₹5-10 LPA",
                "description": "Business Analyst with SQL, Excel, and analytical skills.",
                "apply_link": "https://example.com/apply/4",
                "source": "Sample Data"
            },
            {
                "title": "Web Developer",
                "company": "WebCraft Studios",
                "location": "Chennai, India",
                "salary": "₹4-8 LPA",
                "description": "Frontend developer with HTML, CSS, JavaScript, and React.",
                "apply_link": "https://example.com/apply/5",
                "source": "Sample Data"
            },
            {
                "title": "Data Engineer",
                "company": "DataFlow Systems",
                "location": "Hyderabad, India",
                "salary": "₹7-14 LPA",
                "description": "Data Engineer with Python, SQL, Apache Spark, and cloud experience.",
                "apply_link": "https://example.com/apply/6",
                "source": "Sample Data"
            },
            {
                "title": "ML Engineer",
                "company": "Machine Learning Hub",
                "location": "Bangalore, India",
                "salary": "₹9-16 LPA",
                "description": "ML Engineer with Python, scikit-learn, and MLOps experience.",
                "apply_link": "https://example.com/apply/7",
                "source": "Sample Data"
            },
            {
                "title": "Backend Developer",
                "company": "API Solutions",
                "location": "Gurgaon, India",
                "salary": "₹6-11 LPA",
                "description": "Backend developer with Java, Spring Boot, and microservices.",
                "apply_link": "https://example.com/apply/8",
                "source": "Sample Data"
            },
            {
                "title": "Data Analyst",
                "company": "Analytics Pro",
                "location": "Mumbai, India",
                "salary": "₹5-9 LPA",
                "description": "Data Analyst with Python, R, SQL, and visualization tools.",
                "apply_link": "https://example.com/apply/9",
                "source": "Sample Data"
            },
            {
                "title": "Full Stack Developer",
                "company": "FullStack Solutions",
                "location": "Pune, India",
                "salary": "₹7-13 LPA",
                "description": "Full-stack developer with React, Node.js, and database skills.",
                "apply_link": "https://example.com/apply/10",
                "source": "Sample Data"
            }
        ]
    
    def scrape_linkedin_jobs(self, job_title: str, location: str = "India", max_jobs: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape jobs from LinkedIn Jobs
        
        Args:
            job_title (str): Job title to search for
            location (str): Location to search in
            max_jobs (int): Maximum number of jobs to fetch
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        jobs = []
        try:
            # LinkedIn search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={quote_plus(job_title)}&location={quote_plus(location)}"
            
            logger.info(f"Scraping LinkedIn for: {job_title} in {location}")
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_cards = soup.find_all('div', class_='job-search-card')
            
            for card in job_cards[:max_jobs]:
                try:
                    # Extract job title
                    title_elem = card.find('h3', class_='base-search-card__title')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    # Extract company name
                    company_elem = card.find('h4', class_='base-search-card__subtitle')
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    
                    # Extract location
                    location_elem = card.find('span', class_='job-search-card__location')
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    # Extract salary (if available)
                    salary_elem = card.find('span', class_='job-search-card__salary-info')
                    salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"
                    
                    # Extract job link
                    link_elem = card.find('a', class_='base-card__full-link')
                    apply_link = link_elem['href'] if link_elem and link_elem.get('href') else "#"
                    
                    # Extract description snippet
                    desc_elem = card.find('p', class_='job-search-card__snippet')
                    description = desc_elem.get_text(strip=True) if desc_elem else "No description available"
                    
                    job = {
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "salary": salary,
                        "description": description,
                        "apply_link": apply_link,
                        "source": "LinkedIn"
                    }
                    
                    jobs.append(job)
                    
                except Exception as e:
                    logger.warning(f"Error parsing LinkedIn job card: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs)} jobs from LinkedIn")
            
        except Exception as e:
            logger.error(f"Error scraping LinkedIn: {e}")
        
        return jobs

    def scrape_indeed_jobs(self, job_title: str, location: str = "India", max_jobs: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape jobs from Indeed.com
        
        Args:
            job_title (str): Job title to search for
            location (str): Location to search in
            max_jobs (int): Maximum number of jobs to fetch
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        jobs = []
        try:
            # Indeed search URL
            search_url = f"https://in.indeed.com/jobs?q={quote_plus(job_title)}&l={quote_plus(location)}"
            
            logger.info(f"Scraping Indeed for: {job_title} in {location}")
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in job_cards[:max_jobs]:
                try:
                    # Extract job title
                    title_elem = card.find('h2', class_='jobTitle')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    # Extract company name
                    company_elem = card.find('span', class_='companyName')
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    
                    # Extract location
                    location_elem = card.find('div', class_='companyLocation')
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    # Extract salary (if available)
                    salary_elem = card.find('span', class_='salary-snippet')
                    salary = salary_elem.get_text(strip=True) if salary_elem else "Not specified"
                    
                    # Extract job link
                    link_elem = title_elem.find('a') if title_elem else None
                    apply_link = f"https://in.indeed.com{link_elem['href']}" if link_elem and link_elem.get('href') else "#"
                    
                    # Extract description snippet
                    desc_elem = card.find('div', class_='job-snippet')
                    description = desc_elem.get_text(strip=True) if desc_elem else "No description available"
                    
                    job = {
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "salary": salary,
                        "description": description,
                        "apply_link": apply_link,
                        "source": "Indeed"
                    }
                    
                    jobs.append(job)
                    
                except Exception as e:
                    logger.warning(f"Error parsing job card: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs)} jobs from Indeed")
            
        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")
        
        return jobs
    
    def scrape_naukri_jobs(self, job_title: str, location: str = "India", max_jobs: int = 10) -> List[Dict[str, Any]]:
        """
        Scrape jobs from Naukri.com
        
        Args:
            job_title (str): Job title to search for
            location (str): Location to search in
            max_jobs (int): Maximum number of jobs to fetch
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        jobs = []
        try:
            # Naukri search URL
            search_url = f"https://www.naukri.com/{quote_plus(job_title.lower().replace(' ', '-'))}-jobs-in-{quote_plus(location.lower())}"
            
            logger.info(f"Scraping Naukri for: {job_title} in {location}")
            response = self.session.get(search_url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job listings
            job_cards = soup.find_all('div', class_='jobTuple')
            
            for card in job_cards[:max_jobs]:
                try:
                    # Extract job title
                    title_elem = card.find('a', class_='title')
                    title = title_elem.get_text(strip=True) if title_elem else "N/A"
                    
                    # Extract company name
                    company_elem = card.find('a', class_='subTitle')
                    company = company_elem.get_text(strip=True) if company_elem else "N/A"
                    
                    # Extract location
                    location_elem = card.find('span', class_='ellipsis')
                    job_location = location_elem.get_text(strip=True) if location_elem else location
                    
                    # Extract salary (if available)
                    salary_elem = card.find('span', class_='ellipsis')
                    salary = "Not specified"  # Naukri salary extraction is complex
                    
                    # Extract job link
                    apply_link = title_elem['href'] if title_elem and title_elem.get('href') else "#"
                    
                    # Extract description snippet
                    desc_elem = card.find('div', class_='job-description')
                    description = desc_elem.get_text(strip=True) if desc_elem else "No description available"
                    
                    job = {
                        "title": title,
                        "company": company,
                        "location": job_location,
                        "salary": salary,
                        "description": description,
                        "apply_link": apply_link,
                        "source": "Naukri"
                    }
                    
                    jobs.append(job)
                    
                except Exception as e:
                    logger.warning(f"Error parsing job card: {e}")
                    continue
            
            logger.info(f"Successfully scraped {len(jobs)} jobs from Naukri")
            
        except Exception as e:
            logger.error(f"Error scraping Naukri: {e}")
        
        return jobs
    
    def get_sample_jobs(self, job_title: str, max_jobs: int = 10) -> List[Dict[str, Any]]:
        """
        Get sample job data as fallback.
        
        Args:
            job_title (str): Job title to filter by
            max_jobs (int): Maximum number of jobs to return
            
        Returns:
            List[Dict[str, Any]]: List of sample job postings
        """
        # Filter sample jobs by title similarity
        filtered_jobs = []
        job_title_lower = job_title.lower()
        
        for job in self.sample_jobs:
            if any(keyword in job['title'].lower() for keyword in job_title_lower.split()):
                filtered_jobs.append(job)
        
        # If no matches, return general jobs
        if not filtered_jobs:
            filtered_jobs = self.sample_jobs[:max_jobs]
        
        return filtered_jobs[:max_jobs]
    
    def scrape_jobs(self, job_title: str, location: str = "India", max_jobs: int = 10, use_sample: bool = False) -> List[Dict[str, Any]]:
        """
        Scrape jobs from multiple sources.
        
        Args:
            job_title (str): Job title to search for
            location (str): Location to search in
            max_jobs (int): Maximum number of jobs to fetch
            use_sample (bool): Whether to use sample data instead of scraping
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        if use_sample:
            logger.info("Using sample job data")
            return self.get_sample_jobs(job_title, max_jobs)
        
        all_jobs = []
        
        # Try to scrape from LinkedIn
        try:
            linkedin_jobs = self.scrape_linkedin_jobs(job_title, location, max_jobs // 3)
            all_jobs.extend(linkedin_jobs)
            logger.info(f"LinkedIn: Found {len(linkedin_jobs)} jobs")
        except Exception as e:
            logger.warning(f"LinkedIn scraping failed: {e}")
        
        # Try to scrape from Indeed
        try:
            indeed_jobs = self.scrape_indeed_jobs(job_title, location, max_jobs // 3)
            all_jobs.extend(indeed_jobs)
            logger.info(f"Indeed: Found {len(indeed_jobs)} jobs")
        except Exception as e:
            logger.warning(f"Indeed scraping failed: {e}")
        
        # Try to scrape from Naukri
        try:
            naukri_jobs = self.scrape_naukri_jobs(job_title, location, max_jobs // 3)
            all_jobs.extend(naukri_jobs)
            logger.info(f"Naukri: Found {len(naukri_jobs)} jobs")
        except Exception as e:
            logger.warning(f"Naukri scraping failed: {e}")
        
        # If no jobs found from scraping, use sample data
        if not all_jobs:
            logger.info("No jobs found from scraping, using sample data")
            all_jobs = self.get_sample_jobs(job_title, max_jobs)
        
        # Remove duplicates and limit results
        unique_jobs = []
        seen_titles = set()
        
        for job in all_jobs:
            if job['title'] not in seen_titles:
                unique_jobs.append(job)
                seen_titles.add(job['title'])
                
                if len(unique_jobs) >= max_jobs:
                    break
        
        logger.info(f"Returning {len(unique_jobs)} unique jobs from {len(set(job['source'] for job in unique_jobs))} sources")
        return unique_jobs
    
    def save_jobs_to_file(self, jobs: List[Dict[str, Any]], filename: str = None) -> None:
        """
        Save jobs to a JSON file.
        
        Args:
            jobs (List[Dict[str, Any]]): List of job postings
            filename (str): Filename to save to
        """
        if filename is None:
            filename = self.job_data_path
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(jobs, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Jobs saved to {filename}")
    
    def load_jobs_from_file(self, filename: str = None) -> List[Dict[str, Any]]:
        """
        Load jobs from a JSON file.
        
        Args:
            filename (str): Filename to load from
            
        Returns:
            List[Dict[str, Any]]: List of job postings
        """
        if filename is None:
            filename = self.job_data_path
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                jobs = json.load(f)
            logger.info(f"Loaded {len(jobs)} jobs from {filename}")
            return jobs
        except FileNotFoundError:
            logger.warning(f"File not found: {filename}")
            return []
        except Exception as e:
            logger.error(f"Error loading jobs: {e}")
            return []

def main():
    """
    Test the job scraping functionality.
    """
    scraper = JobScraper()
    
    # Test with sample data
    jobs = scraper.scrape_jobs("Data Scientist", "India", 5, use_sample=True)
    
    print(f"Found {len(jobs)} jobs:")
    for i, job in enumerate(jobs, 1):
        print(f"\n{i}. {job['title']}")
        print(f"   Company: {job['company']}")
        print(f"   Location: {job['location']}")
        print(f"   Salary: {job['salary']}")
        print(f"   Apply: {job['apply_link']}")
        print(f"   Source: {job['source']}")

if __name__ == "__main__":
    main()
