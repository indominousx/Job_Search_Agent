from typing import Any, Dict
import logging
import json
from langchain_core.prompts import ChatPromptTemplate
from app.workflows.state import WorkflowState
from app.services.ai_service import get_llm
from app.schemas.job import StructuredJobSchema, JobMatchScoreSchema

logger = logging.getLogger(__name__)

async def discover_jobs_node(state: WorkflowState) -> WorkflowState:
    """
    Scrapes external job boards or APIs to find new job postings.
    For V1, this is a mocked discovery mechanism.
    """
    logger.info(f"Discovering jobs for user: {state['user_id']}")
    
    mocked_jobs = [
        {
            "raw_text": "We are looking for a Senior Software Engineer with 5+ years of Python experience, FastAPI, and PostgreSQL. Remote work available.",
            "source_url": "https://example.com/job/1"
        },
        {
            "raw_text": "Junior Frontend Developer needed. React, TypeScript, and CSS. Must be located in New York.",
            "source_url": "https://example.com/job/2"
        }
    ]
    return {"discovered_jobs": mocked_jobs}

async def normalize_jobs_node(state: WorkflowState) -> WorkflowState:
    """
    Uses the LLM to structure raw job descriptions into a standard schema.
    """
    discovered_jobs = state.get('discovered_jobs', [])
    logger.info(f"Normalizing {len(discovered_jobs)} jobs")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(StructuredJobSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract the job details from the raw text into the requested structured format. Do not fabricate information. If a field is missing, leave it empty or null."),
        ("human", "Raw Job Posting:\n{text}\nSource URL: {url}")
    ])
    
    chain = prompt | structured_llm
    normalized = []
    
    for job in discovered_jobs:
        try:
            result = await chain.ainvoke({"text": job["raw_text"], "url": job["source_url"]})
            # Ensure the original raw text is preserved for context
            result.original_text = job["raw_text"]
            normalized.append(result.model_dump())
        except Exception as e:
            logger.error(f"Failed to normalize job: {e}")
            
    return {"normalized_jobs": normalized}

async def match_jobs_node(state: WorkflowState) -> WorkflowState:
    """
    Compares normalized jobs against the Candidate Profile to generate fit scores.
    """
    normalized_jobs = state.get('normalized_jobs', [])
    profile = state.get('candidate_profile', {})
    logger.info(f"Matching {len(normalized_jobs)} jobs against Candidate Profile")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(JobMatchScoreSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical recruiter. You are evaluating a Candidate Profile against a Structured Job Posting. Provide an objective score out of 100 on how well the candidate fits the role based on their skills and experience. Be realistic and critical. Only score >= 75 if they are a strong fit. Return the score, an explanation, missing skills, and a boolean is_fit (True if score >= 75)."),
        ("human", "Candidate Profile:\n{profile}\n\nJob Posting:\n{job}")
    ])
    
    chain = prompt | structured_llm
    matched = []
    
    for job in normalized_jobs:
        try:
            result = await chain.ainvoke({
                "profile": json.dumps(profile, indent=2),
                "job": json.dumps(job, indent=2)
            })
            if result.is_fit:
                matched.append({
                    "job": job,
                    "score": result.model_dump()
                })
        except Exception as e:
            logger.error(f"Failed to match job: {e}")
            
    return {"matched_jobs": matched}

import uuid
from app.schemas.application import GeneratedApplicationSchema

async def prepare_application_node(state: WorkflowState) -> WorkflowState:
    """
    Generates tailored application answers and cover letters for matched jobs.
    In a full implementation, this also creates a JobApplication record in the database.
    """
    matched_jobs = state.get('matched_jobs', [])
    profile = state.get('candidate_profile', {})
    logger.info(f"Preparing applications for {len(matched_jobs)} matched jobs")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(GeneratedApplicationSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert career coach writing a highly tailored cover letter and standard job application Q&A on behalf of the candidate. Do not fabricate experience not present in the profile. Answer questions directly and professionally."),
        ("human", "Candidate Profile:\n{profile}\n\nJob Details:\n{job}")
    ])
    
    chain = prompt | structured_llm
    prepared = []
    
    for match in matched_jobs:
        job = match["job"]
        try:
            result = await chain.ainvoke({
                "profile": json.dumps(profile, indent=2),
                "job": json.dumps(job, indent=2)
            })
            
            # In a production setup, we would insert this into the DB here:
            # application = JobApplication(
            #     id=str(uuid.uuid4()),
            #     user_id=state["user_id"],
            #     job_title=job["title"],
            #     company=job["company"],
            #     source_url=job.get("source_url"),
            #     match_score=match["score"]["score"],
            #     cover_letter=result.cover_letter,
            #     generated_qa=result.qa_answers
            # )
            # db.add(application)
            # db.commit()
            
            prepared.append({
                "job": job,
                "application": result.model_dump()
            })
        except Exception as e:
            logger.error(f"Failed to prepare application: {e}")
            
    return {"prepared_applications": prepared}
