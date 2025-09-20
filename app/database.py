from sqlmodel import Session, SQLModel, create_engine

# SQLite database URL
DATABASE_URL = "sqlite:///./app.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)