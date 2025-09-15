from fastapi import FastAPI, HTTPException, status
from sqlmodel import Session, SQLModel, create_engine
from .models import UserCreate, UserRead, User

app = FastAPI()

# In-memory SQLite database
engine = create_engine("sqlite:///")
SQLModel.metadata.create_all(engine)

# Store for tracking used usernames and emails
used_usernames = set()
used_emails = set()
next_user_id = 1

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/ping")
async def ping():
    return {"ping": "pong"}

@app.post("/users/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate) -> UserRead:
    global next_user_id
    
    if user.username in used_usernames:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )
    
    if user.email in used_emails:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    new_user = User(
        id=next_user_id,
        username=user.username,
        email=user.email
    )
    
    used_usernames.add(user.username)
    used_emails.add(user.email)
    next_user_id += 1
    
    return UserRead(**new_user.dict())