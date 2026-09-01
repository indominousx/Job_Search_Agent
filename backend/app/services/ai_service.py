from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.language_models.chat_models import BaseChatModel
from app.core.config import settings

def get_llm(
    gemini_key: Optional[str] = None, 
    groq_key: Optional[str] = None
) -> BaseChatModel:
    """
    Returns an LLM instance with provider fallback logic configured.
    It attempts Gemini first, and falls back to Groq.
    User-provided keys override the system .env keys.
    """
    
    # Resolve API keys (User provided overrides .env)
    g_key = gemini_key or settings.GEMINI_API_KEY
    q_key = groq_key or settings.GROQ_API_KEY
    f_key = settings.FALLBACK_API_KEY

    llms = []

    # 1. Primary: Gemini (1.5 Flash is fast and cheap for parsing/generation)
    if g_key:
        llms.append(
            ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                temperature=0.0, # Zero for strict extraction
                google_api_key=g_key,
                max_retries=2
            )
        )
    elif f_key and settings.FALLBACK_PROVIDER == "gemini":
        llms.append(
            ChatGoogleGenerativeAI(
                model=settings.FALLBACK_MODEL or "gemini-1.5-flash",
                temperature=0.0,
                google_api_key=f_key,
                max_retries=2
            )
        )

    # 2. Fallback: Groq (Llama 3.1 8b is incredibly fast)
    if q_key:
        llms.append(
            ChatGroq(
                model="llama-3.1-8b-instant",
                temperature=0.0,
                groq_api_key=q_key,
                max_retries=2
            )
        )
    elif f_key and settings.FALLBACK_PROVIDER == "groq":
        llms.append(
            ChatGroq(
                model=settings.FALLBACK_MODEL or "llama-3.1-8b-instant",
                temperature=0.0,
                groq_api_key=f_key,
                max_retries=2
            )
        )

    if not llms:
        raise ValueError("No valid LLM configuration found. Please provide an API key.")

    primary_llm = llms[0]
    
    # Apply fallbacks if there are multiple available configurations
    if len(llms) > 1:
        return primary_llm.with_fallbacks(llms[1:])
    
    return primary_llm
