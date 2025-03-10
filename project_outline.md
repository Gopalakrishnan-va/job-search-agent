I'll help you create a LangGraph-compatible structure with cursor rules and agent instructions for the job search system. I'll break this down into separate agents with their specific instructions and a manager agent to orchestrate the workflow.

```python
# manager_agent.py
```
```python
from typing import Dict, List, Optional
from langgraph.graph import Graph
from pydantic import BaseModel

class ManagerAgent:
    """
    Orchestrates the job search workflow by coordinating all specialized agents.
    """
    
    def __init__(self):
        self.state = {
            "resume_parsed": False,
            "jobs_scraped": False,
            "analysis_complete": False,
            "current_phase": "init"
        }

    async def determine_next_step(self, current_state: Dict) -> str:
        """
        Determines the next agent to invoke based on current state
        """
        if not current_state["resume_parsed"]:
            return "RESUME_PARSER"
        elif not current_state["jobs_scraped"]:
            return "JOB_SCRAPER"
        elif not current_state["analysis_complete"]:
            return "RELEVANCE_SCORER"
        else:
            return "COMPLETE"

    SYSTEM_PROMPT = """
    You are an AI Job Search Manager coordinating multiple specialized agents.
    Your role is to:
    1. Track the state of the job search process
    2. Determine which agent should act next
    3. Ensure all necessary information is passed between agents
    4. Maintain the overall quality and relevance of the search

    Follow these steps:
    1. Check current state
    2. Identify next required action
    3. Dispatch appropriate agent
    4. Update state based on results
    5. Continue until search is complete or needs user input
    """
```

```python
# resume_parser_agent.py
```
```python
class ResumeParserAgent:
    """
    Specialized in extracting structured information from resume text.
    """
    
    SYSTEM_PROMPT = """
    You are an AI Resume Parser specialized in extracting key information from resumes.
    
    OBJECTIVE:
    Extract and structure the following information from the resume:
    - Skills (technical and soft skills)
    - Work experience (years and positions)
    - Education
    - Desired role/position
    - Location preferences
    - Industry experience
    
    INSTRUCTIONS:
    1. Analyze the resume text carefully
    2. Identify and categorize all relevant information
    3. Structure the data in the following format:
       {
         "skills": ["skill1", "skill2", ...],
         "experience": {
           "total_years": X,
           "positions": [{
             "title": "...",
             "duration": "...",
             "company": "..."
           }]
         },
         "education": [...],
         "desired_role": "...",
         "location_preference": "...",
         "industry_experience": [...]
       }
    4. Ensure all extracted information is relevant and accurate
    5. Flag any ambiguous or missing critical information
    """

    def parse(self, resume_text: str) -> Dict:
        # Implementation details here
        pass
```

```python
# job_scraper_agent.py
```
```python
class JobScraperAgent:
    """
    Handles job listing collection from various sources.
    """
    
    SYSTEM_PROMPT = """
    You are an AI Job Scraper Agent responsible for collecting relevant job listings.
    
    OBJECTIVE:
    Search and collect job listings from Indeed and LinkedIn based on parsed resume data.
    
    INSTRUCTIONS:
    1. Use the following search parameters from resume data:
       - Primary job title/role
       - Alternative titles
       - Location preferences
       - Experience level
       - Key skills
       
    2. For each job listing, collect:
       - Job title
       - Company name
       - Location (including remote/hybrid status)
       - Required experience
       - Key responsibilities
       - Required skills
       - Salary information (if available)
       - Posted date
       - Application URL
       
    3. Apply initial filtering:
       - Remove duplicates
       - Exclude listings older than 30 days
       - Filter out irrelevant positions
       
    4. Structure data in standardized format for analysis
    """

    async def scrape(self, search_params: Dict) -> List[Dict]:
        # Implementation details here
        pass
```

```python
# relevance_scorer_agent.py
```
```python
class RelevanceScorerAgent:
    """
    Analyzes and scores job listings based on resume match.
    """
    
    SYSTEM_PROMPT = """
    You are an AI Relevance Scorer specialized in matching job listings to candidate profiles.
    
    OBJECTIVE:
    Score job listings based on match quality with candidate profile.
    
    SCORING CRITERIA:
    1. Position Match (30%):
       - Exact title match: 100%
       - Related title: 60-90%
       - Different but relevant: 30-50%
       
    2. Experience & Skills (25%):
       - Required skills match: 0-100%
       - Years of experience match: 0-100%
       
    3. Location (20%):
       - Exact location match: 100%
       - Remote (if preferred): 100%
       - Nearby location: 50-80%
       
    4. Company Match (15%):
       - Industry match: 0-100%
       - Company size preference: 0-100%
       
    5. Additional Factors (10%):
       - Salary match
       - Growth potential
       - Company culture
    
    INSTRUCTIONS:
    1. Compare each job listing against candidate profile
    2. Calculate individual scores for each criterion
    3. Apply weights to calculate final score
    4. Return scored listings with detailed breakdown
    """

    def score_listing(self, job: Dict, candidate_profile: Dict) -> Dict:
        # Implementation details here
        pass
```

```python
# feedback_refiner_agent.py
```
```python
class FeedbackRefinerAgent:
    """
    Processes user feedback to improve search results.
    """
    
    SYSTEM_PROMPT = """
    You are an AI Feedback Refiner that improves job search results based on user feedback.
    
    OBJECTIVE:
    Adjust search parameters and scoring weights based on user feedback.
    
    INSTRUCTIONS:
    1. Analyze user feedback types:
       - Relevance feedback
       - Location preference changes
       - Salary expectations
       - Role specificity
       - Industry preferences
       
    2. Update search parameters:
       - Modify search keywords
       - Adjust location filters
       - Update experience requirements
       
    3. Adjust scoring weights:
       - Increase/decrease importance of matching criteria
       - Update minimum thresholds
       - Modify relevance calculations
       
    4. Provide recommendations for:
       - New search terms
       - Alternative job titles
       - Additional skills to highlight
    """

    def process_feedback(self, feedback: Dict) -> Dict:
        # Implementation details here
        pass
```

```python
# notification_agent.py
```
```python
class NotificationAgent:
    """
    Handles job alerts and application tracking.
    """
    
    SYSTEM_PROMPT = """
    You are an AI Notification Agent managing job search updates and tracking.
    
    OBJECTIVE:
    Keep users informed of new opportunities and track applications.
    
    INSTRUCTIONS:
    1. Monitor for new matching jobs:
       - Check against existing matches
       - Apply relevance threshold
       - Prepare notification content
       
    2. Track applications:
       - Record application dates
       - Monitor status changes
       - Note follow-up requirements
       
    3. Generate updates:
       - Daily job matches
       - Application status changes
       - Upcoming deadlines
       - Follow-up reminders
       
    4. Maintain communication log:
       - Track all notifications
       - Record user interactions
       - Monitor engagement metrics
    """

    async def process_updates(self, updates: List[Dict]) -> None:
        # Implementation details here
        pass
```

```python
# main.py
```
```python
from typing import Dict, List
from langgraph.graph import Graph
from apify_client import ApifyClient

def create_job_search_workflow():
    # Initialize agents
    manager = ManagerAgent()
    resume_parser = ResumeParserAgent()
    job_scraper = JobScraperAgent()
    relevance_scorer = RelevanceScorerAgent()
    feedback_refiner = FeedbackRefinerAgent()
    notification_agent = NotificationAgent()

    # Define workflow graph
    workflow = Graph()
    
    # Add nodes
    workflow.add_node("manager", manager.determine_next_step)
    workflow.add_node("resume_parser", resume_parser.parse)
    workflow.add_node("job_scraper", job_scraper.scrape)
    workflow.add_node("relevance_scorer", relevance_scorer.score_listing)
    workflow.add_node("feedback_refiner", feedback_refiner.process_feedback)
    workflow.add_node("notification", notification_agent.process_updates)

    # Define edges (transitions)
    workflow.add_edge("manager", "resume_parser")
    workflow.add_edge("resume_parser", "job_scraper")
    workflow.add_edge("job_scraper", "relevance_scorer")
    workflow.add_edge("relevance_scorer", "feedback_refiner")
    workflow.add_edge("feedback_refiner", "notification")
    workflow.add_edge("notification", "manager")

    return workflow

# Initialize Apify client
apify_client = ApifyClient(token="your_apify_token")

# Run workflow
async def run_job_search(resume_text: str):
    workflow = create_job_search_workflow()
    initial_state = {
        "resume_text": resume_text,
        "parsed_resume": None,
        "job_listings": [],
        "scored_listings": [],
        "feedback": {},
        "notifications": []
    }
    
    result = await workflow.run(initial_state)
    return result
```

This structure provides:

1. A clear separation of concerns with specialized agents
2. Structured prompts for each agent's specific task
3. Integration with Apify's LangGraph
4. A manager agent to orchestrate the workflow
5. Clear data structures for information passing
6. Feedback loops for continuous improvement

To use this with Apify:

1. Create an Apify actor for each agent
2. Use the Apify client to run actors in sequence
3. Store intermediate results in Apify key-value store
4. Use webhook URLs to chain actor executions
5. Monitor execution using Apify's dashboard

Remember to:
- Add error handling
- Implement rate limiting
- Add logging
- Include input validation
- Add proper authentication
- Implement retry logic
- Add monitoring and alerting

You can extend this further by:
- Adding more specialized agents
- Implementing parallel processing
- Adding more sophisticated feedback loops
- Implementing A/B testing
- Adding performance metrics
- Implementing caching