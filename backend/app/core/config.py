from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Career Application Agent"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # SECURITY
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # DATABASE
    DATABASE_URL: str = "postgresql+psycopg://user:password@localhost/jobagent"
    
    # LLM PROVIDERS
    GEMINI_API_KEY: Optional[str] = None
    GROQ_API_KEY: Optional[str] = None
    FALLBACK_API_KEY: Optional[str] = None
    FALLBACK_PROVIDER: Optional[str] = None
    FALLBACK_MODEL: Optional[str] = None
    
    # RESOURCE MANAGEMENT
    MAX_CONCURRENT_JOBS: int = 2
    
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

settings = Settings()
