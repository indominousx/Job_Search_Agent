from pydantic import BaseModel, Field
from typing import List, Optional

class StructuredJobSchema(BaseModel):
    title: str = Field(description="The job title")
    company: str = Field(description="The company name")
    location: Optional[str] = Field(description="The job location")
    work_model: Optional[str] = Field(description="Work model (e.g., Remote, Hybrid, Onsite)")
    requirements: List[str] = Field(default_factory=list, description="List of explicit job requirements")
    tech_stack: List[str] = Field(default_factory=list, description="List of technologies, languages, or tools required")
    original_text: str = Field(description="The original raw job description text")
    source_url: Optional[str] = Field(default=None, description="The URL to the original job posting")

class JobMatchScoreSchema(BaseModel):
    score: int = Field(description="Match score out of 100 based on candidate fit")
    explanation: str = Field(description="Detailed explanation of why the score was given")
    missing_skills: List[str] = Field(default_factory=list, description="Skills required by the job that the candidate lacks")
    is_fit: bool = Field(description="True if the score is greater than or equal to 75, False otherwise")
