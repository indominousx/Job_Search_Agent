from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AI Career Application Agent API",
    description="Backend API for the AI Career Application Agent (V1)",
    version="1.0.0",
)

# Set up CORS middleware for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.api.api import api_router
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Render requires a health check endpoint."""
    return {"status": "ok"}
