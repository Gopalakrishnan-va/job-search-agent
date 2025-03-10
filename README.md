# Job Search Agent - Apify Actor

An AI-powered job search agent that analyzes your resume and finds matching job opportunities. This agent is built as an Apify actor using LangGraph and LangChain.

## Features

- **Resume Analysis**: Extracts key skills, experience, and qualifications from your resume
- **Job Search**: Searches multiple job platforms (LinkedIn, Indeed) for matching opportunities
- **Relevance Scoring**: Ranks job listings based on match with your resume
- **Detailed Results**: Provides comprehensive information about each job match

## Usage

### Running on Apify Platform

1. Go to the [Job Search Agent](https://console.apify.com/actors/your-username/job-search-agent) on Apify
2. Click "Run"
3. Enter your resume text in the "Resume Text" field
4. (Optional) Configure search preferences:
   - Location: Preferred job location
   - Work Mode: remote, hybrid, onsite, or any
   - Maximum Results: Number of job results to return
5. Click "Start"
6. View your results in the "Dataset" tab

### Input

```json
{
  "resumeText": "Your full resume text here...",
  "searchPreferences": {
    "location": "New York, NY",
    "workMode": "remote",
    "maxResults": 10
  }
}
```

### Output

The actor outputs a JSON object with the following structure:

```json
{
  "query": "Extracted resume information",
  "results": [
    "Job 1 details...",
    "Job 2 details...",
    "..."
  ],
  "timestamp": "2025-03-10T12:34:56.789Z"
}
```

## Local Development

### Prerequisites

- Python 3.11+
- Apify CLI

### Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   APIFY_API_TOKEN=your_apify_api_token
   ```

### Running Locally

```bash
apify run
```

Or with Python directly:

```bash
python -m src.main
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `APIFY_API_TOKEN`: Your Apify API token
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `LINKEDIN_JOBS_ACTOR`: Apify actor ID for LinkedIn jobs search
- `LINKEDIN_DETAIL_ACTOR`: Apify actor ID for LinkedIn job detail
- `INDEED_SCRAPER_ACTOR`: Apify actor ID for Indeed scraper

## License

MIT 