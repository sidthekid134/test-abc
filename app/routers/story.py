"""
Story router for Apollo application.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.models.models import Story, StoryCreate, StoryRead, StoryUpdate, User
from app.database.database import get_session

router = APIRouter()


@router.post("/", response_model=StoryRead)
def create_story(
    *,
    session: Session = Depends(get_session),
    story: StoryCreate
):
    """Create a new story."""
    # Verify author exists if author_id is provided
    if story.author_id:
        author = session.get(User, story.author_id)
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {story.author_id} not found"
            )

    db_story = Story.from_orm(story)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.get("/", response_model=List[StoryRead])
def read_stories(
    *,
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    status: str = None
):
    """Get all stories with optional status filter."""
    query = select(Story)

    if status:
        query = query.where(Story.status == status)

    query = query.offset(skip).limit(limit)
    stories = session.exec(query).all()
    return stories


@router.get("/{story_id}", response_model=StoryRead)
def read_story(*, session: Session = Depends(get_session), story_id: int):
    """Get a specific story by ID."""
    story = session.get(Story, story_id)
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story with ID {story_id} not found"
        )
    return story


@router.patch("/{story_id}", response_model=StoryRead)
def update_story(
    *,
    session: Session = Depends(get_session),
    story_id: int,
    story: StoryUpdate
):
    """Update a story."""
    db_story = session.get(Story, story_id)
    if not db_story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story with ID {story_id} not found"
        )

    # Verify author exists if author_id is being updated
    story_data = story.dict(exclude_unset=True)
    if "author_id" in story_data and story_data["author_id"] is not None:
        author = session.get(User, story_data["author_id"])
        if not author:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {story_data['author_id']} not found"
            )

    # Update the story fields
    for key, value in story_data.items():
        setattr(db_story, key, value)

    # Always update the updated_at field on any update
    from datetime import datetime
    db_story.updated_at = datetime.utcnow()

    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story


@router.delete("/{story_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_story(*, session: Session = Depends(get_session), story_id: int):
    """Delete a story."""
    story = session.get(Story, story_id)
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Story with ID {story_id} not found"
        )

    session.delete(story)
    session.commit()
    return None


@router.get("/author/{author_id}", response_model=List[StoryRead])
def read_author_stories(
    *,
    session: Session = Depends(get_session),
    author_id: int,
    skip: int = 0,
    limit: int = 100
):
    """Get all stories by a specific author."""
    # Verify author exists
    author = session.get(User, author_id)
    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {author_id} not found"
        )

    query = select(Story).where(Story.author_id == author_id).offset(skip).limit(limit)
    stories = session.exec(query).all()
    return stories