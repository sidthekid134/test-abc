from typing import Dict, List, Any, Optional, Tuple
import logging
from datetime import datetime
from copy import deepcopy
from app.models import Todo, TodoCreate, TodoUpdate
from uuid import uuid4

logger = logging.getLogger(__name__)

class InMemoryDB:
    """
    A simple in-memory database for storing todos.
    This will be expanded in future stories to use actual database.
    """
    def __init__(self):
        self._storage: Dict[str, Dict[str, Any]] = {
            "todos": {}  # Dictionary to store todos by their IDs
        }
        logger.info("In-memory database initialized")

    def get_health(self) -> bool:
        """
        Check if the database is healthy.
        
        Returns:
            bool: True if database is operational.
        """
        return True
    
    # Todo CRUD operations
    def create_todo(self, todo_data: TodoCreate) -> Todo:
        """
        Create a new todo item.
        
        Args:
            todo_data: The data for the new todo item.
            
        Returns:
            Todo: The created todo item with generated ID and timestamps.
        """
        # Create a new Todo instance with the provided data
        todo_id = str(uuid4())
        now = datetime.now()
        
        # Convert TodoCreate to dict and add additional fields
        todo_dict = todo_data.model_dump()
        todo_dict.update({
            "id": todo_id,
            "created_at": now,
            "updated_at": now
        })
        
        # Store the todo item
        self._storage["todos"][todo_id] = todo_dict
        logger.info(f"Created todo item with ID: {todo_id}")
        
        # Return a Todo model instance
        return Todo(**todo_dict)
    
    def get_todo(self, todo_id: str) -> Optional[Todo]:
        """
        Get a todo item by ID.
        
        Args:
            todo_id: The ID of the todo item.
            
        Returns:
            Optional[Todo]: The todo item if found, None otherwise.
        """
        todo_dict = self._storage["todos"].get(todo_id)
        if todo_dict is None:
            logger.warning(f"Todo item with ID {todo_id} not found")
            return None
        
        logger.info(f"Retrieved todo item with ID: {todo_id}")
        return Todo(**todo_dict)
    
    def list_todos(self) -> Tuple[List[Todo], int]:
        """
        Get all todo items.
        
        Returns:
            Tuple[List[Todo], int]: A tuple containing the list of todo items and the total count.
        """
        todos = [Todo(**todo_dict) for todo_dict in self._storage["todos"].values()]
        count = len(todos)
        logger.info(f"Retrieved {count} todo items")
        return todos, count
    
    def update_todo(self, todo_id: str, todo_data: TodoUpdate) -> Optional[Todo]:
        """
        Update a todo item.
        
        Args:
            todo_id: The ID of the todo item to update.
            todo_data: The new data for the todo item.
            
        Returns:
            Optional[Todo]: The updated todo item if found, None otherwise.
        """
        todo_dict = self._storage["todos"].get(todo_id)
        if todo_dict is None:
            logger.warning(f"Todo item with ID {todo_id} not found for update")
            return None
        
        # Update only the fields that are provided
        update_data = {k: v for k, v in todo_data.model_dump().items() if v is not None}
        todo_dict.update(update_data)
        
        # Update the updated_at timestamp
        todo_dict["updated_at"] = datetime.now()
        
        # Store the updated todo item
        self._storage["todos"][todo_id] = todo_dict
        logger.info(f"Updated todo item with ID: {todo_id}")
        
        # Return a Todo model instance
        return Todo(**todo_dict)
    
    def delete_todo(self, todo_id: str) -> bool:
        """
        Delete a todo item.
        
        Args:
            todo_id: The ID of the todo item to delete.
            
        Returns:
            bool: True if the todo item was deleted, False otherwise.
        """
        if todo_id not in self._storage["todos"]:
            logger.warning(f"Todo item with ID {todo_id} not found for deletion")
            return False
        
        del self._storage["todos"][todo_id]
        logger.info(f"Deleted todo item with ID: {todo_id}")
        return True

# Create a singleton instance
db = InMemoryDB()