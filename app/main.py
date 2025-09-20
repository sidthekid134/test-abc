from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from .models import get_session

app = FastAPI(
    title="FastAPI Application",
    description="A FastAPI application using SQLModel for database models",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Application"}