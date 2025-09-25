from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from datetime import datetime

from app.database import get_session
from app.models import User, UserCreate, UserRead

# In a real application, you would implement proper password hashing
# For simplicity, we'll just demonstrate the endpoint structure
# You'd typically import auth utilities like:
# from app.auth import get_password_hash, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}},
)


@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    # Check if username already exists
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if email already exists
    existing_email = session.exec(select(User).where(User.email == user.email)).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # In a real application, hash the password:
    # hashed_password = get_password_hash(user.password)
    hashed_password = user.password  # NOT SECURE, JUST FOR DEMO
    
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    
    return db_user


@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=UserRead)
async def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    
    return user