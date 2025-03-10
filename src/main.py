import os
import json
from typing import Dict, Any
from datetime import datetime
from langchain_apify import ApifyActorsTool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from apify import Actor

from .config.settings import APIFY_API_TOKEN, OPENAI_API_KEY, ACTOR_IDS

def extract_resume_essentials(resume_text: str) -> str:
    """Extract only essential information from resume to reduce tokens."""
    import re
    
    # Split resume into sections
    sections = resume_text.split('\n\n')
    essential_info = []
    
    for section in sections:
        # Keep only relevant sections and clean them
        if any(keyword in section.lower() for keyword in 
               ['experience', 'skills', 'education', 'summary', 'location']):
            # Remove extra whitespace and formatting
            cleaned_section = re.sub(r'\s+', ' ', section).strip()
            # Remove any special characters
            cleaned_section = re.sub(r'[^\w\s,.-]', '', cleaned_section)
            if cleaned_section:
                essential_info.append(cleaned_section)
    
    # Join sections with clear separators
    return ' | '.join(essential_info)

def create_job_search_tools():
    """Create tools for job searching using Apify actors."""
    
    # Set up environment variables
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    os.environ["APIFY_API_TOKEN"] = APIFY_API_TOKEN
    
    # Initialize LLM with reduced tokens
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        max_tokens=4000,
        temperature=0.7
    )
    
    # Create Apify tools with descriptions
    linkedin_jobs = ApifyActorsTool(
        ACTOR_IDS["linkedin_jobs_search"],
        description="Search for jobs on LinkedIn with keywords and location"
    )
    linkedin_detail = ApifyActorsTool(
        ACTOR_IDS["linkedin_job_detail"],
        description="Get detailed information about a specific LinkedIn job"
    )
    indeed_scraper = ApifyActorsTool(
        ACTOR_IDS["indeed_scraper"],
        description="Search for jobs on Indeed with keywords and location"
    )
    
    # Combine tools
    tools = [linkedin_jobs, linkedin_detail, indeed_scraper]
    
    # Create agent executor
    return create_react_agent(llm, tools)

async def run_job_search(resume_text: str, search_preferences: Dict = None) -> Dict[str, Any]:
    """Run the job search workflow with the given resume."""
    try:
        # Extract essential information from resume
        essential_resume = extract_resume_essentials(resume_text)
        print(f"Extracted essential resume information ({len(essential_resume)} chars)")
        
        # Create agent with tools
        agent_executor = create_job_search_tools()
        print("Created job search agent with tools")
        
        # Prepare search preferences
        preferences = ""
        if search_preferences:
            if search_preferences.get("location"):
                preferences += f"Location preference: {search_preferences['location']}\n"
            if search_preferences.get("workMode") and search_preferences["workMode"] != "any":
                preferences += f"Work mode preference: {search_preferences['workMode']}\n"
            if search_preferences.get("maxResults"):
                max_results = search_preferences["maxResults"]
            else:
                max_results = 5
        else:
            max_results = 5
        
        # Prepare the search message (more concise)
        search_message = f"""Resume: {essential_resume}

{preferences}
Task: Find {max_results} best matching jobs.
1. Extract: role, skills, location
2. Search: Use LinkedIn/Indeed
3. Details: Get full info for best matches
4. Return: For each job list:
   - Title
   - Company
   - Location
   - Match score (0-100)
   - Key requirements
   - URL"""
        
        print("Starting job search...")
        # Run the agent
        results = []
        async for state in agent_executor.astream(
            input={
                "messages": [
                    HumanMessage(content=search_message)
                ]
            },
            stream_mode="values"
        ):
            if "messages" in state:
                message = state["messages"][-1]
                results.append(message)
                print(".", end="", flush=True)  # Progress indicator
        
        print("\nSearch completed!")
        
        return {
            "query": essential_resume,
            "results": [msg.content for msg in results if msg.content.strip()],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        error_msg = f"Error during job search: {str(e)}"
        print(f"\n{error_msg}")
        return {
            "error": error_msg,
            "query": essential_resume if 'essential_resume' in locals() else None,
            "results": [],
            "timestamp": datetime.now().isoformat()
        }

async def main():
    """Main entry point for the Apify actor."""
    # Initialize the Actor
    async with Actor:
        # Get input
        actor_input = await Actor.get_input() or {}
        
        # Extract resume text from input
        resume_text = actor_input.get("resumeText", "")
        if not resume_text:
            await Actor.fail("No resume text provided")
            return
        
        # Extract search preferences
        search_preferences = actor_input.get("searchPreferences", {})
        
        # Run job search
        print("Starting job search with Apify actor...")
        result = await run_job_search(resume_text, search_preferences)
        
        # Push data to dataset
        await Actor.push_data(result)
        
        # Set output
        await Actor.set_value("OUTPUT", result)
        
        print("Job search completed successfully!")

if __name__ == "__main__":
    import asyncio
    
    # Run the actor
    asyncio.run(main()) 