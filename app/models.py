from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime
from .database import Base


class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"


class TaskPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskCategory(str, enum.Enum):
    work = "work"
    personal = "personal"
    health = "health"
    finance = "finance"
    education = "education"
    other = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationship with Task model
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    
    # Relationship with UserPreference model
    preferences = relationship("UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    priority = Column(Enum(TaskPriority), default=TaskPriority.medium)
    category = Column(Enum(TaskCategory), default=TaskCategory.other)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    # Foreign key to User model
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship with User model
    user = relationship("User", back_populates="tasks")


class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    default_task_view = Column(String(50), default="all")
    default_sort_field = Column(String(50), default="created_at")
    default_sort_direction = Column(String(4), default="desc")
    theme = Column(String(20), default="light")
    notifications_enabled = Column(Boolean, default=True)
    
    # Foreign key to User model
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    
    # Relationship with User model
    user = relationship("User", back_populates="preferences")