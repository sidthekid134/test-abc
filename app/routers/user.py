"""
User router for Apollo application.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.models import User, UserCreate, UserRead, UserUpdate
from app.database.database import get_session
from app.utils.security import get_password_hash, verify_password

router = APIRouter()


@router.post("/", response_model=UserRead)
def create_user(*, session: Session = Depends(get_session), user: UserCreate):
    """Create a new user."""
    db_user = session.exec(
        select(User).where(User.email == user.email)
    ).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead])
def read_users(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """Get all users."""
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users


@router.get("/{user_id}", response_model=UserRead)
def read_user(*, session: Session = Depends(get_session), user_id: int):
    """Get a specific user by ID."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user: UserUpdate
):
    """Update a user."""
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    user_data = user.dict(exclude_unset=True)

    if "password" in user_data:
        password = user_data.pop("password")
        user_data["hashed_password"] = get_password_hash(password)

    for key, value in user_data.items():
        setattr(db_user, key, value)

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(*, session: Session = Depends(get_session), user_id: int):
    """Delete a user."""
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )

    session.delete(user)
    session.commit()
    return None