from typing import Dict, Any
from .base import BaseAgent

class FeedbackRefinerAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Feedback Refiner Agent responsible for:
        1. Processing user feedback
        2. Adjusting search parameters
        3. Improving match quality
        """

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process user feedback and refine search."""
        # For initial testing, just pass through
        return state 