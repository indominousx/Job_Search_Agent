from fastapi import APIRouter, BackgroundTasks
from app.api.endpoints import resume
import asyncio
import sys
import os

# Import the run_cron function we built earlier to reuse its logic
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scripts.run_cron import run_cron

api_router = APIRouter()
api_router.include_router(resume.router, prefix="/resume", tags=["resume"])

@api_router.post("/cron/run")
async def trigger_workflow(background_tasks: BackgroundTasks):
    """
    Triggers the LangGraph workflow for all users.
    Intended to be hit by an external free cron service (like cron-job.org).
    """
    background_tasks.add_task(asyncio.run, run_cron())
    return {"message": "Workflow triggered in the background successfully."}
