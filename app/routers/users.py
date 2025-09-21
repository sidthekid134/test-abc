from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import EmailStr

from app.database import get_session
from app.models import User, UserCreate, UserRead, UserUpdate
from app.auth import (
    get_password_hash, 
    authenticate_user, 
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    Token,
    get_current_active_user
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    # Check if username already exists
    username_query = select(User).where(User.username == user_data.username)
    existing_user = await session.exec(username_query)
    if existing_user.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    email_query = select(User).where(User.email == user_data.email)
    existing_email = await session.exec(email_query)
    if existing_email.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    """OAuth2 compatible token login, get an access token for future requests."""
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get information about the currently authenticated user."""
    return current_user

@router.get("/{user_id}", response_model=UserRead)
async def read_user(
    user_id: int, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get user by ID (only accessible to authenticated users)."""
    query = select(User).where(User.id == user_id)
    result = await session.exec(query)
    user = result.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    return user

@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get list of users (only accessible to authenticated users)."""
    query = select(User).offset(skip).limit(limit)
    result = await session.exec(query)
    users = result.all()
    return users