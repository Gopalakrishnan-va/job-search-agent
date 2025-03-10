from typing import Dict, Any
from .base import BaseAgent

class RelevanceScorerAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Relevance Scorer Agent responsible for:
        1. Analyzing job details against resume
        2. Calculating match scores
        3. Ranking job opportunities
        """

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process and score job listings."""
        # For initial testing, we'll just pass through the jobs
        state["analysis_complete"] = True
        return state 