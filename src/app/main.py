from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from .models import create_db_and_tables, get_session
from .models import Item, ItemCreate, ItemRead

app = FastAPI(title="FastAPI Application")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application"}

@app.post("/items/", response_model=ItemRead)
def create_item(*, session: Session = Depends(get_session), item: ItemCreate):
    db_item = Item.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@app.get("/items/", response_model=List[ItemRead])
def read_items(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items

@app.get("/items/{item_id}", response_model=ItemRead)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item