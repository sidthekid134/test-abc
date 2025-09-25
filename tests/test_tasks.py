import json
import pytest
from datetime import datetime
from fastapi import status

from app.models import Task


def test_create_task(client):
    # Test creating a task
    task_data = {
        "title": "New Task",
        "description": "This is a new task",
        "priority": 3,
        "due_date": datetime.utcnow().isoformat()
    }
    
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["priority"] == task_data["priority"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_validation_error(client):
    # Test validation error - priority out of range
    task_data = {
        "title": "Invalid Task",
        "priority": 10  # Should be between 1-5
    }
    
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_tasks(client, test_tasks):
    # Test reading all tasks
    response = client.get("/tasks/")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 3  # We created 3 test tasks in the fixture
    

def test_read_tasks_filter_completed(client, test_tasks):
    # Test filtering tasks by completion status
    response = client.get("/tasks/?completed=true")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["completed"] is True


def test_read_tasks_filter_priority(client, test_tasks):
    # Test filtering tasks by priority
    response = client.get("/tasks/?priority=2")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert data[0]["priority"] == 2


def test_read_tasks_filter_title(client, test_tasks):
    # Test filtering tasks by title
    response = client.get("/tasks/?title=Task 1")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 1
    assert "Task 1" in data[0]["title"]


def test_read_tasks_sort(client, test_tasks):
    # Test sorting tasks
    response = client.get("/tasks/?sort_by=priority&sort_order=asc")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert len(data) == 3
    assert data[0]["priority"] == 1
    assert data[1]["priority"] == 2
    assert data[2]["priority"] == 3


def test_read_task(client, test_tasks):
    # Test reading a specific task
    task_id = test_tasks[0].id
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == test_tasks[0].title


def test_read_task_not_found(client):
    # Test reading a non-existent task
    response = client.get("/tasks/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_task(client, test_tasks):
    # Test updating a task
    task_id = test_tasks[0].id
    update_data = {
        "title": "Updated Task Title",
        "completed": True
    }
    
    response = client.patch(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == update_data["title"]
    assert data["completed"] == update_data["completed"]
    assert data["description"] == test_tasks[0].description  # Unchanged field


def test_update_task_validation_error(client, test_tasks):
    # Test validation error during update - priority out of range
    task_id = test_tasks[0].id
    update_data = {
        "priority": 10  # Should be between 1-5
    }
    
    response = client.patch(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_update_task_not_found(client):
    # Test updating a non-existent task
    update_data = {"title": "This Task Doesn't Exist"}
    response = client.patch("/tasks/9999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task(client, test_tasks):
    # Test deleting a task
    task_id = test_tasks[0].id
    
    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_200_OK
    
    # Try to fetch the deleted task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_task_not_found(client):
    # Test deleting a non-existent task
    response = client.delete("/tasks/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND