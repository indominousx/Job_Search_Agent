from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.models.base import Base

class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    
    # We optionally link to the resume used
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=True)

    job_title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    source_url = Column(String, nullable=True)
    
    match_score = Column(Integer, nullable=False)
    status = Column(String, default="PREPARED") # PREPARED, APPLIED, REJECTED
    
    generated_qa = Column(JSONB, nullable=True)
    cover_letter = Column(Text, nullable=True)

    user = relationship("User", back_populates="applications")
    resume = relationship("Resume")
