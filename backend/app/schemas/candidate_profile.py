from pydantic import BaseModel, Field
from typing import List, Optional

class CandidateProfileSchema(BaseModel):
    name: Optional[str] = Field(description="Full name of the candidate")
    education: List[str] = Field(default_factory=list, description="List of degrees and universities attended")
    experience: List[str] = Field(default_factory=list, description="List of past roles and companies")
    projects: List[str] = Field(default_factory=list, description="List of significant projects worked on")
    skills: List[str] = Field(default_factory=list, description="General skills")
    programming_languages: List[str] = Field(default_factory=list, description="Programming languages known")
    frameworks: List[str] = Field(default_factory=list, description="Software frameworks and libraries")
    databases: List[str] = Field(default_factory=list, description="Databases used")
    cloud: List[str] = Field(default_factory=list, description="Cloud platforms and services used")
    ai_ml: List[str] = Field(default_factory=list, description="AI/ML tools, models, and libraries")
    certifications: List[str] = Field(default_factory=list, description="Certifications achieved")
    achievements: List[str] = Field(default_factory=list, description="Awards and achievements")
    domains: List[str] = Field(default_factory=list, description="Industry domains worked in (e.g., Finance, Healthcare)")
