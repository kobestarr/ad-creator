import re
from urllib.parse import urlparse, parse_qs, urlunparse
from typing import Dict, List, Optional, Any
import json

class LinkedInURLCleaner:
    """
    Cleans and transforms LinkedIn URLs from company/profile links to direct job posting links.
    """
    
    @staticmethod
    def extract_job_id_from_url(url: str) -> Optional[str]:
        """
        Extract job ID from various LinkedIn URL formats.
        """
        patterns = [
            r'/jobs/view/[^/]*?(\d+)',
            r'/jobs/[^/]*?(\d+)',
            r'jobId=(\d+)',
            r'currentJobId=(\d+)',
            r'job/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def clean_company_name(company_url: str) -> str:
        """
        Extract clean company name from LinkedIn company URL.
        """
        # Extract company name from URL like '/company/mango-analytics-ai'
        match = re.search(r'/company/([^/?]+)', company_url)
        if match:
            company_name = match.group(1)
            # Clean up the company name
            company_name = company_name.replace('-', ' ').title()
            return company_name
        return "Unknown Company"
    
    @staticmethod
    def build_job_url(job_title: str, company_name: str, job_id: str) -> str:
        """
        Build a clean LinkedIn job posting URL.
        """
        # Clean job title for URL
        clean_title = re.sub(r'[^\w\s-]', '', job_title.lower())
        clean_title = re.sub(r'[-\s]+', '-', clean_title).strip('-')
        
        # Clean company name for URL
        clean_company = re.sub(r'[^\w\s-]', '', company_name.lower())
        clean_company = re.sub(r'[-\s]+', '-', clean_company).strip('-')
        
        return f"https://www.linkedin.com/jobs/view/{clean_title}-at-{clean_company}-{job_id}"
    
    @staticmethod
    def clean_linkedin_url(url: str, job_title: str = "", company_name: str = "") -> str:
        """
        Main function to clean LinkedIn URLs.
        """
        if not url:
            return ""
        
        # Try to extract job ID from existing URL
        job_id = LinkedInURLCleaner.extract_job_id_from_url(url)
        
        if job_id and job_title and company_name:
            # If we have all components, build clean URL
            return LinkedInURLCleaner.build_job_url(job_title, company_name, job_id)
        elif job_id:
            # If we only have job ID, return basic job URL
            return f"https://www.linkedin.com/jobs/view/{job_id}"
        
        # If it's a company URL, we can't convert it without job ID
        if '/company/' in url:
            return url  # Return original as we can't convert without job ID
        
        return url


class LinkedInDataCleaner:
    """
    Comprehensive data cleaning pipeline for LinkedIn job data.
    """
    
    def __init__(self):
        self.url_cleaner = LinkedInURLCleaner()
        
        # Common job title normalizations
        self.title_mappings = {
            r'sr\.': 'Senior',
            r'jr\.': 'Junior',
            r'sr\b': 'Senior',
            r'jr\b': 'Junior',
            r'software engr': 'Software Engineer',
            r'software eng': 'Software Engineer',
            r'swe\b': 'Software Engineer',
            r'dev\b': 'Developer',
            r'data engr': 'Data Engineer',
            r'data eng': 'Data Engineer',
            r'ml engr': 'Machine Learning Engineer',
            r'ml eng': 'Machine Learning Engineer',
            r'ai engr': 'AI Engineer',
            r'ai eng': 'AI Engineer',
        }
        
        # Company name cleanups
        self.company_mappings = {
            r'inc\b\.?': '',
            r'llc\b\.?': '',
            r'ltd\b\.?': '',
            r'corp\b\.?': '',
            r'corporation\b': '',
            r'company\b': '',
        }
    
    def clean_job_title(self, title: str) -> str:
        """
        Clean and normalize job titles.
        """
        if not title:
            return "Unknown Position"
        
        title = title.strip()
        
        # Apply title mappings in specific order to avoid conflicts
        title_mappings_ordered = [
            (r'\bsr\b\.?', 'Senior'),
            (r'\bjr\b\.?', 'Junior'),
            (r'software engr\b', 'Software Engineer'),
            (r'software eng\b', 'Software Engineer'),
            (r'\bswe\b', 'Software Engineer'),
            (r'\bdev\b', 'Developer'),
            (r'data engr\b', 'Data Engineer'),
            (r'data eng\b', 'Data Engineer'),
            (r'ml engr\b', 'Machine Learning Engineer'),
            (r'ml eng\b', 'Machine Learning Engineer'),
            (r'ai engr\b', 'AI Engineer'),
            (r'ai eng\b', 'AI Engineer'),
        ]
        
        for pattern, replacement in title_mappings_ordered:
            title = re.sub(pattern, replacement, title, flags=re.IGNORECASE)
        
        # Capitalize words properly (but handle common exceptions)
        exceptions = {'and', 'or', 'the', 'in', 'at', 'to', 'for', 'of', 'with', 'by', 'on', 'as', 'a', 'an'}
        words = title.split()
        capitalized_words = []
        for i, word in enumerate(words):
            if i == 0 or i == len(words) - 1 or word.lower() not in exceptions:
                capitalized_words.append(word.capitalize())
            else:
                capitalized_words.append(word.lower())
        title = ' '.join(capitalized_words)
        
        return title
    
    def clean_company_name(self, company: str) -> str:
        """
        Clean and normalize company names.
        """
        if not company:
            return "Unknown Company"
        
        company = company.strip()
        
        # Apply company mappings in specific order
        company_mappings_ordered = [
            (r'\binc\b\.?', ''),
            (r'\bllc\b\.?', ''),
            (r'\bltd\b\.?', ''),
            (r'\bcorp\b\.?', ''),
            (r'\bcorporation\b', ''),
            (r'\bcompany\b', ''),
        ]
        
        for pattern, replacement in company_mappings_ordered:
            company = re.sub(pattern, replacement, company, flags=re.IGNORECASE)
        
        # Remove extra whitespace and clean up
        company = re.sub(r'\s+', ' ', company).strip()
        company = re.sub(r'\s*-\s*$', '', company).strip()
        
        # Clean up whitespace and punctuation
        company = re.sub(r'[^\w\s&-]', '', company)
        company = re.sub(r'\s+', ' ', company).strip()
        
        return company
    
    def extract_location_info(self, location: str) -> Dict[str, str]:
        """
        Extract structured location information.
        """
        if not location:
            return {"city": "Unknown", "state": "Unknown", "country": "Unknown"}
        
        location = location.strip()
        parts = [part.strip() for part in location.split(',')]
        
        result = {"city": "Unknown", "state": "Unknown", "country": "Unknown"}
        
        if len(parts) >= 1:
            result["city"] = parts[0]
        if len(parts) >= 2:
            result["state"] = parts[1]
        if len(parts) >= 3:
            result["country"] = parts[2]
        
        return result
    
    def clean_salary_info(self, salary: str) -> Dict[str, Any]:
        """
        Extract and clean salary information.
        """
        if not salary:
            return {"min": None, "max": None, "currency": "USD", "period": "yearly"}
        
        salary = salary.lower().strip()
        
        # Extract numbers
        numbers = re.findall(r'[\d,]+', salary)
        numbers = [int(num.replace(',', '')) for num in numbers]
        
        # Determine currency
        currency = "USD"
        if any(curr in salary for curr in ['€', 'eur', 'euro']):
            currency = "EUR"
        elif any(curr in salary for curr in ['£', 'gbp', 'pound']):
            currency = "GBP"
        elif any(curr in salary for curr in ['$', 'usd']):
            currency = "USD"
        
        # Determine period
        period = "yearly"
        if any(p in salary for p in ['hour', 'hr']):
            period = "hourly"
        elif any(p in salary for p in ['month', 'mo']):
            period = "monthly"
        elif any(p in salary for p in ['week', 'wk']):
            period = "weekly"
        
        min_salary = max_salary = None
        if len(numbers) >= 2:
            min_salary, max_salary = sorted(numbers)[:2]
        elif len(numbers) == 1:
            min_salary = max_salary = numbers[0]
        
        return {
            "min": min_salary,
            "max": max_salary,
            "currency": currency,
            "period": period
        }
    
    def clean_job_description(self, description: str) -> str:
        """
        Clean and format job descriptions.
        """
        if not description:
            return ""
        
        # Remove excessive whitespace
        description = re.sub(r'\s+', ' ', description)
        
        # Remove common HTML tags if present
        description = re.sub(r'<[^>]+>', '', description)
        
        # Remove LinkedIn-specific tracking parameters
        description = re.sub(r'\?trk=[^\s]+', '', description)
        
        return description.strip()
    
    def determine_seniority_level(self, title: str) -> str:
        """
        Determine seniority level from job title.
        """
        if not title:
            return "Unknown"
        
        title_lower = title.lower()
        
        if any(level in title_lower for level in ['senior', 'sr.', 'lead', 'principal', 'staff']):
            return "Senior"
        elif any(level in title_lower for level in ['junior', 'jr.', 'entry', 'associate', 'intern']):
            return "Junior"
        elif any(level in title_lower for level in ['manager', 'director', 'vp', 'head of', 'chief']):
            return "Management"
        elif any(level in title_lower for level in ['executive', 'ceo', 'cto', 'cfo', 'coo']):
            return "Executive"
        else:
            return "Mid-level"
    
    def clean_job_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main cleaning function that processes raw LinkedIn job data.
        """
        cleaned_data = {}
        
        # Clean job title
        cleaned_data['job_title'] = self.clean_job_title(raw_data.get('job_title', ''))
        
        # Clean company name
        cleaned_data['company_name'] = self.clean_company_name(raw_data.get('company_name', ''))
        
        # Clean job URL
        original_url = raw_data.get('job_url', '')
        if original_url:
            cleaned_data['job_url'] = self.url_cleaner.clean_linkedin_url(
                original_url,
                cleaned_data['job_title'],
                cleaned_data['company_name']
            )
        else:
            cleaned_data['job_url'] = ""
        
        # Extract location info
        location = raw_data.get('location', '')
        cleaned_data['location'] = self.extract_location_info(location)
        
        # Clean salary information
        salary = raw_data.get('salary', '')
        cleaned_data['salary'] = self.clean_salary_info(salary)
        
        # Clean job description
        cleaned_data['job_description'] = self.clean_job_description(
            raw_data.get('job_description', '')
        )
        
        # Determine seniority level
        cleaned_data['seniority_level'] = self.determine_seniority_level(
            cleaned_data['job_title']
        )
        
        # Add metadata
        cleaned_data['employment_type'] = raw_data.get('employment_type', 'Full-time')
        cleaned_data['industry'] = raw_data.get('industry', 'Technology')
        cleaned_data['posted_date'] = raw_data.get('posted_date', '')
        cleaned_data['application_deadline'] = raw_data.get('application_deadline', '')
        
        # Add processing timestamp
        from datetime import datetime
        cleaned_data['processed_at'] = datetime.now().isoformat()
        
        return cleaned_data
    
    def process_batch(self, raw_jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Process a batch of job listings.
        """
        cleaned_jobs = []
        
        for job in raw_jobs:
            try:
                cleaned_job = self.clean_job_data(job)
                cleaned_jobs.append(cleaned_job)
            except Exception as e:
                print(f"Error processing job: {e}")
                continue
        
        return cleaned_jobs


def main():
    """
    Example usage of the LinkedIn data cleaning pipeline.
    """
    # Sample raw LinkedIn job data
    raw_jobs = [
        {
            "job_title": "Sr. Software Engr",
            "company_name": "Mango Analytics AI, Inc.",
            "job_url": "https://www.linkedin.com/company/mango-analytics-ai?trk=public_jobs_topcard-org-name",
            "location": "San Francisco, CA, United States",
            "salary": "$120,000 - $180,000 per year",
            "job_description": "We are looking for a Senior Software Engineer... <br><br>Requirements: 5+ years experience",
            "employment_type": "Full-time",
            "industry": "Technology",
            "posted_date": "2024-01-15",
            "application_deadline": "2024-02-15"
        },
        {
            "job_title": "Jr. Data Scientist",
            "company_name": "TechCorp LLC",
            "job_url": "https://www.linkedin.com/jobs/view/1234567890",
            "location": "New York, NY",
            "salary": "$80,000 - $100,000",
            "job_description": "Entry-level data scientist position...",
            "employment_type": "Full-time",
            "industry": "Finance",
            "posted_date": "2024-01-10",
            "application_deadline": "2024-02-10"
        }
    ]
    
    # Initialize cleaner
    cleaner = LinkedInDataCleaner()
    
    # Process the batch
    cleaned_jobs = cleaner.process_batch(raw_jobs)
    
    # Display results
    print("=== Cleaned LinkedIn Job Data ===\n")
    for i, job in enumerate(cleaned_jobs, 1):
        print(f"Job {i}:")
        print(f"  Title: {job['job_title']}")
        print(f"  Company: {job['company_name']}")
        print(f"  URL: {job['job_url']}")
        print(f"  Location: {job['location']['city']}, {job['location']['state']}")
        print(f"  Seniority: {job['seniority_level']}")
        print(f"  Salary: ${job['salary']['min']:,} - ${job['salary']['max']:,} {job['salary']['currency']} {job['salary']['period']}")
        print(f"  Description: {job['job_description'][:100]}...")
        print()


if __name__ == "__main__":
    main()