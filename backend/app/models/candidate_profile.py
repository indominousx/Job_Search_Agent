import uuid
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.models.base import Base

class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), unique=True, nullable=False)
    resume_id: Mapped[str] = mapped_column(String, ForeignKey("resumes.id"), nullable=False)
    
    # Store the extracted structured data directly in a JSONB column for flexibility
    # This aligns well with LLM JSON outputs and allows arbitrary nesting without complex schemas
    parsed_data: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    user = relationship("User")
    resume = relationship("Resume")
