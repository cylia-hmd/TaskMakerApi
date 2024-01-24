import json
import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 404
    assert isinstance(response.json(), list)

def test_create_task():
    task_data = {
        "title": "medical appointment",
        "description": "medical appointment",
        "owner": "Cylia",
        "completed": True
    }

    response = client.post("/tasks", json=task_data)
    assert response.status_code == 404  
    assert "id" in response.json()

def test_get_task_by_id():
    task_id = str(uuid.uuid4())
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404  


def test_modify_task():
    task_id = str(uuid.uuid4())
    modified_task_data = {
        "title": "appointment modified",
        "description": "medical appointment",
        "owner": "Yuna",
        "completed": False 
    }

    response = client.patch(f"/tasks/{task_id}", json=modified_task_data)
    assert response.status_code == 404  

def test_delete_task():
    task_id = str(uuid.uuid4())
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 404  