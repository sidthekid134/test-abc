from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, UserPreference
from ..schemas import (
    User as UserSchema,
    UserUpdate,
    UserPreference as UserPreferenceSchema,
    UserPreferenceCreate,
    UserPreferenceUpdate,
    UserWithPreferences
)
from ..utils.auth import get_current_active_user, get_password_hash

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)


@router.get("/me", response_model=UserWithPreferences)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get current authenticated user's information with preferences
    """
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update current user's profile information
    """
    # Check if the username is being changed and if it's already taken
    if user_update.username and user_update.username != current_user.username:
        db_user = db.query(User).filter(User.username == user_update.username).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
    
    # Check if the email is being changed and if it's already taken
    if user_update.email and user_update.email != current_user.email:
        db_user = db.query(User).filter(User.email == user_update.email).first()
        if db_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Update user fields
    if user_update.username:
        current_user.username = user_update.username
    if user_update.email:
        current_user.email = user_update.email
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    if user_update.password:
        current_user.hashed_password = get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/me/preferences", response_model=UserPreferenceSchema)
async def read_user_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's preferences
    """
    # If the user doesn't have preferences yet, create default preferences
    if not current_user.preferences:
        preferences = UserPreference(user_id=current_user.id)
        db.add(preferences)
        db.commit()
        db.refresh(preferences)
        return preferences
    
    return current_user.preferences


@router.post("/me/preferences", response_model=UserPreferenceSchema)
async def create_user_preferences(
    preferences: UserPreferenceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create preferences for current user
    """
    # Check if user already has preferences
    if current_user.preferences:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User preferences already exist. Use PUT to update."
        )
    
    # Create new preferences
    db_preferences = UserPreference(
        **preferences.dict(),
        user_id=current_user.id
    )
    
    db.add(db_preferences)
    db.commit()
    db.refresh(db_preferences)
    
    return db_preferences


@router.put("/me/preferences", response_model=UserPreferenceSchema)
async def update_user_preferences(
    preferences: UserPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update current user's preferences
    """
    # If the user doesn't have preferences yet, create new preferences
    if not current_user.preferences:
        db_preferences = UserPreference(
            **preferences.dict(),
            user_id=current_user.id
        )
        db.add(db_preferences)
    else:
        # Update existing preferences
        db_preferences = current_user.preferences
        
        for key, value in preferences.dict(exclude_unset=True).items():
            setattr(db_preferences, key, value)
    
    db.commit()
    db.refresh(db_preferences)
    
    return db_preferences