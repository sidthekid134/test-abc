import uvicorn
import logging
from app.main import app
from app.database import create_db_and_tables

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup"""
    logger.info("Starting up Task Management API")
    create_db_and_tables()

if __name__ == "__main__":
    logger.info("Starting Task Management API server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)