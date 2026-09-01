import io
from pypdf import PdfReader
import docx
from app.schemas.candidate_profile import CandidateProfileSchema
from langchain_core.prompts import ChatPromptTemplate
# You would import your preferred LLM wrapper here (e.g., from langchain_google_genai import ChatGoogleGenerativeAI)
# For now we'll mock the LLM call or leave a placeholder.

def extract_text_from_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_docx(file_bytes: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_bytes))
    return "\n".join([para.text for para in doc.paragraphs])

def extract_resume_text(file_bytes: bytes, content_type: str) -> str:
    if "pdf" in content_type.lower():
        return extract_text_from_pdf(file_bytes)
    elif "word" in content_type.lower() or "officedocument" in content_type.lower():
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file type")

from app.services.ai_service import get_llm

def parse_resume_to_profile(text: str) -> CandidateProfileSchema:
    """
    Calls the LLM to extract a CandidateProfileSchema from the text.
    In V1, this should use LangChain's with_structured_output().
    """
    llm = get_llm()
    structured_llm = llm.with_structured_output(CandidateProfileSchema)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical recruiter. Extract the following information from the provided resume text into a structured format. Do NOT fabricate or infer any information not explicitly present in the text. If a field is missing, leave it empty."),
        ("human", "Resume Text:\n{text}")
    ])
    
    chain = prompt | structured_llm
    return chain.invoke({"text": text})
