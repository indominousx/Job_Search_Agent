import asyncio
import logging
import sys
import os

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base import Base
from app.db.session import engine, get_db
from app.workflows.graph import get_compiled_graph
from psycopg_pool import ConnectionPool
from langgraph.checkpoint.postgres import PostgresSaver
from app.core.config import settings
from app.models.user import User
from app.models.candidate_profile import CandidateProfile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_cron():
    """
    Cron job entrypoint.
    Runs the LangGraph orchestration independently of the FastAPI web server.
    Optimized for memory constraints by only loading what's necessary.
    """
    logger.info("Starting JobAgent Cron Workflow...")
    
    try:
        # Load all active users who have a profile
        # Note: using a sync session for brevity here in the cron script, 
        # but could use async SQLAlchemy session.
        db_gen = get_db()
        db = next(db_gen)
        
        users = db.query(User).filter(User.is_active == True).all()
        logger.info(f"Found {len(users)} active users.")

        # Initialize the PostgresSaver for the graph using psycopg_pool
        # (Assuming settings.DATABASE_URL is a valid postgresql:// URI)
        # We must convert asyncpg/postgresql+psycopg to standard postgresql:// if needed by psycopg
        db_url = settings.DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")
        
        with ConnectionPool(db_url) as pool:
            checkpointer = PostgresSaver(pool)
            checkpointer.setup()
            
            graph = get_compiled_graph(checkpointer)
            
            for user in users:
                # Find candidate profile for user
                profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()
                if not profile:
                    logger.warning(f"User {user.id} has no candidate profile. Skipping.")
                    continue
                
                logger.info(f"Executing workflow for User {user.id}")
                
                # Execute graph
                config = {"configurable": {"thread_id": f"cron-{user.id}"}}
                
                initial_state = {
                    "user_id": user.id,
                    "candidate_profile": profile.parsed_data,
                    "discovered_jobs": [],
                    "normalized_jobs": [],
                    "matched_jobs": [],
                    "prepared_applications": []
                }
                
                # We use ainvoke to trigger the async graph execution
                final_state = await graph.ainvoke(initial_state, config=config)
                
                logger.info(f"Completed workflow for User {user.id}. Prepared {len(final_state.get('prepared_applications', []))} applications.")

    except Exception as e:
        logger.error(f"Cron execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(run_cron())
