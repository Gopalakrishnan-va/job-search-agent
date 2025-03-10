import os
from typing import Dict
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
# This is useful for local development
if os.path.exists(".env"):
    load_dotenv()

# API Keys - Apify will automatically provide these in the actor environment
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN") or os.getenv("APIFY_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI Model Configuration
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Using the cheapest model by default

# Apify Actor IDs
ACTOR_IDS: Dict[str, str] = {
    "linkedin_jobs_search": os.getenv("LINKEDIN_JOBS_ACTOR", "apimaestro/linkedin-jobs-scraper-api"),
    "linkedin_job_detail": os.getenv("LINKEDIN_DETAIL_ACTOR", "apimaestro/linkedin-job-detail"),
    "indeed_scraper": os.getenv("INDEED_SCRAPER_ACTOR", "misceres/indeed-scraper")
}

# Job Search Settings
JOB_SEARCH_CONFIG = {
    "initial_results_per_source": int(os.getenv("INITIAL_RESULTS_PER_SOURCE", "5")),
    "detail_fetch_threshold": float(os.getenv("DETAIL_FETCH_THRESHOLD", "0.6")),
    "max_details_to_fetch": int(os.getenv("MAX_DETAILS_TO_FETCH", "5")),
    "max_days_old": int(os.getenv("MAX_DAYS_OLD", "30"))
}

# Scoring weights for initial filtering
INITIAL_SCORING_WEIGHTS = {
    "title_match": float(os.getenv("WEIGHT_TITLE_MATCH", "0.4")),
    "location_match": float(os.getenv("WEIGHT_LOCATION_MATCH", "0.3")),
    "company_relevance": float(os.getenv("WEIGHT_COMPANY_RELEVANCE", "0.2")),
    "posting_date": float(os.getenv("WEIGHT_POSTING_DATE", "0.1"))
}

# Detailed scoring weights
FINAL_SCORING_WEIGHTS = {
    "position_match": float(os.getenv("WEIGHT_POSITION_MATCH", "0.25")),
    "skills_experience": float(os.getenv("WEIGHT_SKILLS_EXPERIENCE", "0.30")),
    "location": float(os.getenv("WEIGHT_LOCATION", "0.15")),
    "company_match": float(os.getenv("WEIGHT_COMPANY_MATCH", "0.15")),
    "salary_match": float(os.getenv("WEIGHT_SALARY_MATCH", "0.10")),
    "benefits": float(os.getenv("WEIGHT_BENEFITS", "0.05"))
}

# System settings
RETRY_ATTEMPTS = int(os.getenv("RETRY_ATTEMPTS", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))  # seconds 