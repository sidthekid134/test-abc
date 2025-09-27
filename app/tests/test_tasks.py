from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
import json
from datetime import datetime, timedelta

from app.main import app
from app.database import get_session
from app.models.task import Task, TaskStatus, TaskPriority

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
    # Test basic task creation
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Test Task", 
            "description": "Test Description",
            "priority": "high",
            "tags": ["test", "example"]
        },
    )
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["priority"] == "high"
    assert data["tags"] == ["test", "example"]
    assert data["status"] == "todo"
    assert "id" in data
    
    # Test validation - empty title
    response = client.post(
        "/api/tasks/",
        json={"title": "", "description": "Test Description"},
    )
    assert response.status_code == 400
    assert "Title cannot be empty" in response.json()["detail"]

def test_read_tasks(client: TestClient, session: Session):
    # Create some test tasks with different statuses and priorities
    task_1 = Task(title="Task 1", description="Description 1", status=TaskStatus.TODO, priority=TaskPriority.LOW)
    task_2 = Task(title="Task 2", description="Description 2", status=TaskStatus.IN_PROGRESS, priority=TaskPriority.MEDIUM)
    task_3 = Task(title="Task 3", description="Description 3", status=TaskStatus.DONE, priority=TaskPriority.HIGH)
    session.add(task_1)
    session.add(task_2)
    session.add(task_3)
    session.commit()

    # Test reading all tasks
    response = client.get("/api/tasks/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 3
    
    # Test filtering by status
    response = client.get("/api/tasks/?status=todo")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 1"
    
    # Test filtering by priority
    response = client.get("/api/tasks/?priority=high")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 3"
    
    # Test search functionality
    response = client.get("/api/tasks/?search=Description 2")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 2"

def test_read_task(client: TestClient, session: Session):
    # Create a test task
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()

    # Test reading a specific task
    response = client.get(f"/api/tasks/{task.id}")
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    
    # Test reading a non-existent task
    response = client.get(f"/api/tasks/999")
    assert response.status_code == 404
    assert "Task with ID 999 not found" in response.json()["detail"]

def test_update_task(client: TestClient, session: Session):
    # Create a test task
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()

    # Test updating task title
    response = client.patch(
        f"/api/tasks/{task.id}",
        json={"title": "Updated Task"},
    )
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Updated Task"
    assert data["description"] == "Test Description"
    
    # Test updating multiple fields
    response = client.patch(
        f"/api/tasks/{task.id}",
        json={
            "description": "Updated Description",
            "status": "in_progress",
            "priority": "high"
        },
    )
    data = response.json()
    assert response.status_code == 200
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated Description"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"
    
    # Test validation - empty title
    response = client.patch(
        f"/api/tasks/{task.id}",
        json={"title": ""},
    )
    assert response.status_code == 400
    assert "Title cannot be empty" in response.json()["detail"]
    
    # Test updating a non-existent task
    response = client.patch(
        f"/api/tasks/999",
        json={"title": "This won't work"},
    )
    assert response.status_code == 404
    assert "Task with ID 999 not found" in response.json()["detail"]

def test_delete_task(client: TestClient, session: Session):
    # Create a test task
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()

    # Test deleting a task
    response = client.delete(f"/api/tasks/{task.id}")
    assert response.status_code == 204

    # Verify task is deleted
    response = client.get(f"/api/tasks/{task.id}")
    assert response.status_code == 404
    
    # Test deleting a non-existent task
    response = client.delete(f"/api/tasks/999")
    assert response.status_code == 404
    assert "Task with ID 999 not found" in response.json()["detail"]

def test_complete_task(client: TestClient, session: Session):
    # Create a test task
    task = Task(title="Test Task", description="Test Description")
    session.add(task)
    session.commit()

    # Test marking task as complete
    response = client.post(f"/api/tasks/{task.id}/complete")
    data = response.json()
    assert response.status_code == 200
    assert data["status"] == "done"
    assert data["completed_at"] is not None
    
    # Test completing a non-existent task
    response = client.post(f"/api/tasks/999/complete")
    assert response.status_code == 404
    assert "Task with ID 999 not found" in response.json()["detail"]

def test_get_tasks_by_status(client: TestClient, session: Session):
    # Create tasks with different statuses
    task_1 = Task(title="Task 1", status=TaskStatus.TODO)
    task_2 = Task(title="Task 2", status=TaskStatus.IN_PROGRESS)
    task_3 = Task(title="Task 3", status=TaskStatus.DONE)
    session.add(task_1)
    session.add(task_2)
    session.add(task_3)
    session.commit()

    # Test filtering tasks by status
    response = client.get("/api/tasks/status/todo")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 1"
    
    response = client.get("/api/tasks/status/in_progress")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 2"
    
    response = client.get("/api/tasks/status/done")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 3"

def test_get_tasks_by_priority(client: TestClient, session: Session):
    # Create tasks with different priorities
    task_1 = Task(title="Task 1", priority=TaskPriority.LOW)
    task_2 = Task(title="Task 2", priority=TaskPriority.MEDIUM)
    task_3 = Task(title="Task 3", priority=TaskPriority.HIGH)
    session.add(task_1)
    session.add(task_2)
    session.add(task_3)
    session.commit()

    # Test filtering tasks by priority
    response = client.get("/api/tasks/priority/low")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 1"
    
    response = client.get("/api/tasks/priority/medium")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 2"
    
    response = client.get("/api/tasks/priority/high")
    data = response.json()
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]["title"] == "Task 3"

def test_task_due_date(client: TestClient):
    # Create task with due date
    tomorrow = (datetime.utcnow() + timedelta(days=1)).isoformat()
    
    response = client.post(
        "/api/tasks/",
        json={
            "title": "Task with Due Date",
            "description": "This task has a due date",
            "due_date": tomorrow
        },
    )
    
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "Task with Due Date"
    assert data["due_date"] is not None