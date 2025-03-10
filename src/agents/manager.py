from typing import Dict, Any
from .base import BaseAgent

class ManagerAgent(BaseAgent):
    def __init__(self):
        super().__init__(None)  # Manager doesn't need Apify client
    
    def _get_system_prompt(self) -> str:
        return """
        Manager Agent responsible for:
        1. Coordinating the job search workflow
        2. Determining next steps based on current state
        3. Handling transitions between agents
        """
    
    async def determine_next_step(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Determine the next step in the workflow."""
        if not state.get("resume_parsed", False):
            state["next_step"] = "resume_parser"
        elif not state.get("jobs_scraped", False):
            state["next_step"] = "job_scraper"
        elif not state.get("analysis_complete", False):
            state["next_step"] = "relevance_scorer"
        else:
            state["next_step"] = "complete"
        return state
    
    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the current state."""
        return await self.determine_next_step(state) 