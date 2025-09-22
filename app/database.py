from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class InMemoryDB:
    """
    A simple in-memory database for storing todos.
    This will be expanded in future stories to use actual database.
    """
    def __init__(self):
        self._storage: Dict[str, Any] = {}
        logger.info("In-memory database initialized")

    def get_health(self) -> bool:
        """
        Check if the database is healthy.
        
        Returns:
            bool: True if database is operational.
        """
        return True

# Create a singleton instance
db = InMemoryDB()