from pydantic import BaseModel, Field
from typing import Dict

class GeneratedApplicationSchema(BaseModel):
    cover_letter: str = Field(description="A highly tailored cover letter for the job based on the candidate profile")
    qa_answers: Dict[str, str] = Field(description="Key-value pairs of common application questions (e.g., 'Why do you want to work here?', 'What is your greatest strength?') and the personalized answers.")
