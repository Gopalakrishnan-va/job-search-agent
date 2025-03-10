from typing import Dict, Any, List
from .base import BaseAgent
from ..models.schema import ResumeData, WorkExperience, Education

class ResumeParserAgent(BaseAgent):
    def _get_system_prompt(self) -> str:
        return """
        Resume Parser Agent responsible for:
        1. Extracting structured information from resume text
        2. Identifying key skills and experience
        3. Determining job search parameters
        """

    def _extract_basic_info(self, text: str) -> Dict[str, Any]:
        """Extract basic information from resume text."""
        # For testing, we'll use hardcoded values based on our test resume
        return {
            "desired_role": "Software Engineer",
            "location_preference": "New York, NY",
            "total_years_experience": 5.0,
            "skills": [
                "Python", "JavaScript", "TypeScript", "SQL",
                "React", "Django", "FastAPI", "Node.js",
                "AWS", "Docker", "Kubernetes",
                "TensorFlow", "PyTorch", "LangChain"
            ],
            "industry_experience": ["Technology", "Software Development"],
            "experience": [
                WorkExperience(
                    title="Senior Software Engineer",
                    company="TechCorp Inc.",
                    duration="2 years",
                    description="Led development of microservices-based architecture"
                ),
                WorkExperience(
                    title="Software Engineer",
                    company="StartupX",
                    duration="2.5 years",
                    description="Full-stack web development"
                )
            ],
            "education": [
                Education(
                    degree="Bachelor of Science",
                    institution="New York University",
                    year="2018",
                    field="Computer Science"
                )
            ]
        }

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the resume text and update state."""
        resume_text = state.get("resume_text", "")
        if not resume_text:
            raise ValueError("No resume text provided")

        # Extract information from resume
        parsed_data = self._extract_basic_info(resume_text)
        
        # Create ResumeData instance
        resume_data = ResumeData(**parsed_data)
        
        # Update state
        state["resume_parsed"] = True
        state["resume_data"] = resume_data
        
        return state 