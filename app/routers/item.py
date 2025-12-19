"""
Item router for Apollo application.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.models import Item, ItemCreate, ItemRead, ItemUpdate, User
from app.database.database import get_session

router = APIRouter()


@router.post("/", response_model=ItemRead)
def create_item(
    *,
    session: Session = Depends(get_session),
    item: ItemCreate
):
    """Create a new item."""
    # Verify owner exists if owner_id is provided
    if item.owner_id:
        owner = session.get(User, item.owner_id)
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {item.owner_id} not found"
            )

    db_item = Item.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.get("/", response_model=List[ItemRead])
def read_items(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """Get all items."""
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items


@router.get("/{item_id}", response_model=ItemRead)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    """Get a specific item by ID."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )
    return item


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    *,
    session: Session = Depends(get_session),
    item_id: int,
    item: ItemUpdate
):
    """Update an item."""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )

    # Verify owner exists if owner_id is being updated
    item_data = item.dict(exclude_unset=True)
    if "owner_id" in item_data and item_data["owner_id"] is not None:
        owner = session.get(User, item_data["owner_id"])
        if not owner:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {item_data['owner_id']} not found"
            )

    for key, value in item_data.items():
        setattr(db_item, key, value)

    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    """Delete an item."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found"
        )

    session.delete(item)
    session.commit()
    return None