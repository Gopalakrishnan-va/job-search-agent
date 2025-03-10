from typing import Dict, Any
from .base import BaseAgent

class NotificationAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Notification Agent responsible for:
        1. Tracking job application status
        2. Sending notifications
        3. Managing communication
        """

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process notifications and updates."""
        # For initial testing, just pass through
        return state 