"""
Migration script to create users table

Revision ID: 001
Create Date: 2025-09-22
Description: Create users table

"""
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Database connection settings
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/todo_app"
)

def upgrade():
    logger.info("Starting migration: Creating users table")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Create metadata object
    metadata = MetaData()
    
    # Define users table
    users = Table(
        'users', 
        metadata,
        Column('id', Integer, primary_key=True, index=True),
        Column('email', String, unique=True, index=True, nullable=False),
        Column('username', String, unique=True, index=True, nullable=False),
        Column('hashed_password', String, nullable=False),
        Column('is_active', Boolean, default=True),
        Column('is_superuser', Boolean, default=False),
        Column('created_at', DateTime(timezone=True), server_default=func.now()),
        Column('updated_at', DateTime(timezone=True), onupdate=func.now()),
    )
    
    # Create table
    metadata.create_all(engine)
    logger.info("Migration completed: Users table created successfully")

def downgrade():
    logger.info("Starting downgrade: Dropping users table")
    
    # Create SQLAlchemy engine
    engine = create_engine(DATABASE_URL)
    
    # Create metadata object
    metadata = MetaData()
    
    # Reflect existing tables
    metadata.reflect(bind=engine)
    
    # Get users table
    users = metadata.tables.get('users')
    
    # Drop table if it exists
    if users is not None:
        users.drop(engine)
        logger.info("Downgrade completed: Users table dropped successfully")
    else:
        logger.warning("Users table does not exist, nothing to downgrade")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python 001_create_users_table.py [upgrade|downgrade]")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == 'upgrade':
        upgrade()
    elif action == 'downgrade':
        downgrade()
    else:
        print(f"Unknown action: {action}")
        print("Usage: python 001_create_users_table.py [upgrade|downgrade]")
        sys.exit(1)