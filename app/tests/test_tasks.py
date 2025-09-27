from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models.task import Task

# Setup test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_task(client: TestClient):
    response = client.post(
        "/api/tasks/",
        json={"title": "Test Task", "description": "Test Description"},
    )
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert "id" in data

def test_read_tasks(client: TestClient, session: Session):
    # Create some test tasks
    task_1 = Task(title="Task 1", description="Description 1")
    task_2 = Task(title="Task 2", description="Description 2")
    session.add(task_1)
    session.add(task_2)
    session.commit()

    response = client.get("/api/tasks/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"
    assert data[1]["title"] == "Task 2"

def test_read_task(client: TestClient, session: Session):
    # Create a test task
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()

    response = client.get(f"/api/tasks/{task.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"

def test_update_task(client: TestClient, session: Session):
    # Create a test task
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()

    response = client.patch(
        f"/api/tasks/{task.id}",
        json={"title": "Updated Task"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Updated Task"
    assert data["description"] == "Test Description"

def test_delete_task(client: TestClient, session: Session):
    # Create a test task
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()

    response = client.delete(f"/api/tasks/{task.id}")
    assert response.status_code == 204

    response = client.get(f"/api/tasks/{task.id}")
    assert response.status_code == 404