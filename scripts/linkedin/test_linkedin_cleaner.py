#!/usr/bin/env python3
"""
Test script and usage examples for the LinkedIn URL cleaner and data pipeline.
"""

import json
from linkedin_url_cleaner import LinkedInURLCleaner, LinkedInDataCleaner

def test_url_cleaning():
    """Test the URL cleaning functionality."""
    print("=== Testing URL Cleaning ===\n")
    
    url_cleaner = LinkedInURLCleaner()
    
    test_cases = [
        {
            "input": "https://www.linkedin.com/company/mango-analytics-ai?trk=public_jobs_topcard-org-name",
            "job_title": "Java Developer",
            "company_name": "Mango Analytics",
            "expected_job_id": None  # No job ID in company URL
        },
        {
            "input": "https://www.linkedin.com/jobs/view/java-developer-at-mango-analytics-4368116790",
            "job_title": "Java Developer",
            "company_name": "Mango Analytics",
            "expected_job_id": "4368116790"
        },
        {
            "input": "https://www.linkedin.com/jobs/view/1234567890/?trk=public_jobs_topcard-title",
            "job_title": "Senior Software Engineer",
            "company_name": "Tech Corp",
            "expected_job_id": "1234567890"
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}:")
        print(f"  Input URL: {test['input']}")
        print(f"  Job Title: {test['job_title']}")
        print(f"  Company: {test['company_name']}")
        
        # Test job ID extraction
        job_id = url_cleaner.extract_job_id_from_url(test['input'])
        print(f"  Extracted Job ID: {job_id}")
        
        # Test URL cleaning
        cleaned_url = url_cleaner.clean_linkedin_url(
            test['input'], 
            test['job_title'], 
            test['company_name']
        )
        print(f"  Cleaned URL: {cleaned_url}")
        
        # Test URL building
        if job_id:
            built_url = url_cleaner.build_job_url(
                test['job_title'], 
                test['company_name'], 
                job_id
            )
            print(f"  Built URL: {built_url}")
        
        print()

def test_data_cleaning():
    """Test the data cleaning pipeline."""
    print("=== Testing Data Cleaning Pipeline ===\n")
    
    cleaner = LinkedInDataCleaner()
    
    # Sample raw data that simulates real LinkedIn scraping results
    raw_job_data = {
        "job_title": "sr. software engr - backend systems",
        "company_name": "innovative tech solutions, inc.",
        "job_url": "https://www.linkedin.com/company/innovative-tech-solutions?trk=public_jobs_topcard-org-name",
        "location": "austin, texas, united states",
        "salary": "$95,000 - $140,000 per year + equity",
        "job_description": "We're seeking a talented backend engineer to join our growing team... <br><br>Requirements: <ul><li>5+ years Python experience</li><li>AWS expertise</li></ul>",
        "employment_type": "Full-time",
        "industry": "Technology",
        "posted_date": "2024-01-20",
        "application_deadline": "2024-02-20"
    }
    
    print("Original Raw Data:")
    print(json.dumps(raw_job_data, indent=2))
    print("\n" + "="*50 + "\n")
    
    # Clean the data
    cleaned_data = cleaner.clean_job_data(raw_job_data)
    
    print("Cleaned Data:")
    print(json.dumps(cleaned_data, indent=2))
    print()

def test_batch_processing():
    """Test batch processing of multiple jobs."""
    print("=== Testing Batch Processing ===\n")
    
    cleaner = LinkedInDataCleaner()
    
    # Sample batch of raw job data
    batch_data = [
        {
            "job_title": "Jr. ML Engineer",
            "company_name": "DataCorp Analytics LTD",
            "job_url": "https://www.linkedin.com/jobs/view/9876543210",
            "location": "Seattle, WA, USA",
            "salary": "$75,000 - $95,000 annually",
            "job_description": "Entry-level machine learning position...",
            "employment_type": "Full-time",
            "industry": "AI/ML",
            "posted_date": "2024-01-18",
            "application_deadline": "2024-02-18"
        },
        {
            "job_title": "Lead Software Architect",
            "company_name": "CloudTech Inc.",
            "job_url": "https://www.linkedin.com/company/cloudtech?trk=public_jobs_topcard-org-name",
            "location": "Denver, Colorado",
            "salary": "$150,000 - $200,000 + bonus",
            "job_description": "Senior architect role for cloud infrastructure...",
            "employment_type": "Full-time",
            "industry": "Cloud Computing",
            "posted_date": "2024-01-15",
            "application_deadline": "2024-02-15"
        },
        {
            "job_title": "Data Scientist - NLP",
            "company_name": "AI Innovations Corp",
            "job_url": "https://www.linkedin.com/jobs/view/data-scientist-at-ai-innovations-1122334455",
            "location": "Boston, MA",
            "salary": "$110,000 - $160,000 per year",
            "job_description": "Natural language processing specialist...",
            "employment_type": "Full-time",
            "industry": "Artificial Intelligence",
            "posted_date": "2024-01-12",
            "application_deadline": "2024-02-12"
        }
    ]
    
    print(f"Processing {len(batch_data)} jobs...\n")
    
    # Process the batch
    cleaned_jobs = cleaner.process_batch(batch_data)
    
    # Display results
    for i, job in enumerate(cleaned_jobs, 1):
        print(f"Job {i}: {job['job_title']} at {job['company_name']}")
        print(f"  Seniority: {job['seniority_level']}")
        print(f"  Location: {job['location']['city']}, {job['location']['state']}")
        print(f"  Salary Range: ${job['salary']['min']:,} - ${job['salary']['max']:,}")
        print(f"  Clean URL: {job['job_url']}")
        print(f"  Industry: {job['industry']}")
        print()

def test_edge_cases():
    """Test edge cases and error handling."""
    print("=== Testing Edge Cases ===\n")
    
    cleaner = LinkedInDataCleaner()
    
    edge_cases = [
        {
            "name": "Empty Data",
            "data": {}
        },
        {
            "name": "Minimal Data",
            "data": {
                "job_title": "Software Engineer",
                "company_name": "Tech Co"
            }
        },
        {
            "name": "Malformed URL",
            "data": {
                "job_title": "Developer",
                "company_name": "Test Corp",
                "job_url": "not-a-valid-url",
                "salary": "negotiable"
            }
        },
        {
            "name": "International Location",
            "data": {
                "job_title": "Senior Developer",
                "company_name": "Global Tech",
                "location": "Toronto, Ontario, Canada",
                "salary": "CAD 100,000 - 150,000"
            }
        }
    ]
    
    for case in edge_cases:
        print(f"Testing: {case['name']}")
        try:
            result = cleaner.clean_job_data(case['data'])
            print(f"  Result: Success")
            print(f"  Title: {result['job_title']}")
            print(f"  Company: {result['company_name']}")
            print(f"  URL: {result['job_url']}")
            print(f"  Location: {result['location']}")
        except Exception as e:
            print(f"  Error: {e}")
        print()

def generate_sales_ready_output():
    """Generate sales-ready output format."""
    print("=== Sales-Ready Output Format ===\n")
    
    cleaner = LinkedInDataCleaner()
    
    # Sample high-value prospect
    prospect_data = {
        "job_title": "VP of Engineering",
        "company_name": "ScaleTech Solutions Inc.",
        "job_url": "https://www.linkedin.com/jobs/view/vp-engineering-at-scaletech-solutions-9988776655",
        "location": "San Francisco, California, United States",
        "salary": "$200,000 - $300,000 + equity + benefits",
        "job_description": "We are seeking a visionary VP of Engineering to lead our technical teams and drive our product strategy...",
        "employment_type": "Full-time",
        "industry": "Enterprise Software",
        "posted_date": "2024-01-22",
        "application_deadline": "2024-03-22"
    }
    
    cleaned_prospect = cleaner.clean_job_data(prospect_data)
    
    # Create sales-ready summary
    sales_summary = {
        "prospect_name": f"{cleaned_prospect['job_title']} at {cleaned_prospect['company_name']}",
        "linkedin_url": cleaned_prospect['job_url'],
        "location": f"{cleaned_prospect['location']['city']}, {cleaned_prospect['location']['state']}",
        "seniority_level": cleaned_prospect['seniority_level'],
        "industry": cleaned_prospect['industry'],
        "salary_range": f"${cleaned_prospect['salary']['min']:,} - ${cleaned_prospect['salary']['max']:,}",
        "employment_type": cleaned_prospect['employment_type'],
        "posted_date": cleaned_prospect['posted_date'],
        "key_qualifications": cleaned_prospect['job_description'][:200] + "...",
        "sales_notes": f"High-value {cleaned_prospect['seniority_level']} position in {cleaned_prospect['industry']}. "
                      f"Located in {cleaned_prospect['location']['city']} tech hub. "
                      f"Competitive salary range indicates company investment in talent."
    }
    
    print("Sales-Ready Prospect Summary:")
    print(json.dumps(sales_summary, indent=2))

if __name__ == "__main__":
    # Run all tests
    test_url_cleaning()
    test_data_cleaning()
    test_batch_processing()
    test_edge_cases()
    generate_sales_ready_output()
    
    print("=== All Tests Completed ===")
    print("\nTo use this in your project:")
    print("1. Import: from linkedin_url_cleaner import LinkedInDataCleaner")
    print("2. Initialize: cleaner = LinkedInDataCleaner()")
    print("3. Process data: cleaned_job = cleaner.clean_job_data(raw_job_data)")
    print("4. Process batch: cleaned_jobs = cleaner.process_batch(list_of_jobs)")