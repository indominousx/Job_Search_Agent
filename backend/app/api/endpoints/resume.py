from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.resume import Resume
from app.models.candidate_profile import CandidateProfile
from app.services.resume_parser import extract_resume_text, parse_resume_to_profile

router = APIRouter()

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
    # current_user: User = Depends(get_current_user) # To be implemented
):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX are supported.")

    file_bytes = await file.read()
    
    # 1. Create/Update Resume Record
    # For now, we use a dummy user_id since auth isn't fully wired up yet
    dummy_user_id = "user-123" 
    
    # Disable previous resumes
    db.query(Resume).filter(Resume.user_id == dummy_user_id).update({"is_active": False})
    
    new_resume = Resume(
        user_id=dummy_user_id,
        filename=file.filename,
        content_type=file.content_type,
        file_data=file_bytes,
        is_active=True
    )
    db.add(new_resume)
    db.flush() # To get new_resume.id

    # 2. Parse text
    try:
        text = extract_resume_text(file_bytes, file.content_type)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to parse resume: {e}")

    # 3. Extract Profile using LLM
    profile_data = parse_resume_to_profile(text)

    # 4. Save Candidate Profile
    # Delete old profile if exists
    db.query(CandidateProfile).filter(CandidateProfile.user_id == dummy_user_id).delete()
    
    new_profile = CandidateProfile(
        user_id=dummy_user_id,
        resume_id=new_resume.id,
        parsed_data=profile_data.model_dump()
    )
    db.add(new_profile)
    db.commit()

    return {"message": "Resume processed successfully", "profile": profile_data}
