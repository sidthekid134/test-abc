import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.database import get_session
from app.models import Task, TaskCreate


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
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
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "todo"
    }
    
    response = client.post("/api/tasks", json=task_data)
    data = response.json()
    
    assert response.status_code == 201
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_read_tasks(client: TestClient, session: Session):
    # Create test tasks
    task1 = Task(title="Task 1", description="Description 1")
    task2 = Task(title="Task 2", description="Description 2")
    
    session.add(task1)
    session.add(task2)
    session.commit()
    
    response = client.get("/api/tasks")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["title"] == task1.title
    assert data[1]["title"] == task2.title


def test_read_task(client: TestClient, session: Session):
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()
    
    response = client.get(f"/api/tasks/{task.id}")
    data = response.json()
    
    assert response.status_code == 200
    assert data["title"] == task.title
    assert data["description"] == task.description
    assert data["id"] == task.id


def test_update_task(client: TestClient, session: Session):
    task = Task(title="Old Title", description="Old Description")
    session.add(task)
    session.commit()
    
    update_data = {
        "title": "Updated Title",
        "description": "Updated Description"
    }
    
    response = client.put(f"/api/tasks/{task.id}", json=update_data)
    data = response.json()
    
    assert response.status_code == 200
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    
    # Verify database was updated
    updated_task = session.get(Task, task.id)
    assert updated_task.title == update_data["title"]
    assert updated_task.description == update_data["description"]


def test_delete_task(client: TestClient, session: Session):
    task = Task(title="Task to delete")
    session.add(task)
    session.commit()
    
    task_id = task.id
    response = client.delete(f"/api/tasks/{task_id}")
    
    assert response.status_code == 204
    
    # Verify task was deleted
    deleted_task = session.get(Task, task_id)
    assert deleted_task is None