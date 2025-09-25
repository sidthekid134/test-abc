import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_session
from app.models import Task, User


@pytest.fixture(name="engine")
def engine_fixture():
    # Create in-memory SQLite database for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(engine, session):
    # Override the get_session dependency to use the test database
    def get_test_session():
        yield session
        
    app.dependency_overrides[get_session] = get_test_session
    
    with TestClient(app) as client:
        yield client
    
    # Clear the override after the test
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session):
    # Create a test user
    user = User(
        username="testuser",
        email="test@example.com",
        hashed_password="password123"  # Not secure, just for testing
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_tasks")
def test_tasks_fixture(session, test_user):
    # Create some test tasks
    tasks = [
        Task(
            title="Test Task 1",
            description="Description for test task 1",
            priority=1,
            owner_id=test_user.id
        ),
        Task(
            title="Test Task 2",
            description="Description for test task 2",
            priority=2,
            owner_id=test_user.id
        ),
        Task(
            title="Test Task 3",
            description="Description for test task 3",
            priority=3,
            owner_id=test_user.id,
            completed=True
        )
    ]
    for task in tasks:
        session.add(task)
    session.commit()
    
    for task in tasks:
        session.refresh(task)
    
    return tasks