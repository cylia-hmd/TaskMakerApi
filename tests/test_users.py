import uuid
from fastapi.testclient import TestClient
from pytest import fixture
from main import app
from classes.schema_dto import User, UserNoID

@fixture
def test_app():
    return app

@fixture
def test_client(test_app):
    return TestClient(test_app)

@fixture
def create_user():
    users = []

    def _create_user(email: str, username: str, password: str):
        new_user = UserNoID(username=username, email=email, password=password)
        new_user.id = str(uuid.uuid4())
        users.append(new_user)
        return new_user

    return _create_user

def test_get_users(test_client, create_user):
    user1 = create_user(username="user1", email="cy@gmail.com", password="6025")
    user2 = create_user(username="user2", email="lune@gmail.com", password="12345")
    user3 = create_user(username="user3", email="kay@gmail.com", password="kay")

    response = test_client.get("/users")
    assert response.status_code == 404
    assert response.json() == [user.dict() for user in [user1, user2, user3]]

def test_create_user(test_client, create_user):
    new_user_data = {"email": "new_user@example.com", "username": "new_user", "password": "new_password"}
    response = test_client.post("/users", json=new_user_data)
    assert response.status_code == 404
    assert response.json()["username"] == new_user_data["username"]
    assert response.json()["email"] == new_user_data["email"]
    assert response.json()["password"] == new_user_data["password"]

def test_get_user_by_id(test_client, create_user):
    user = create_user(email="test@example.com", username="test_user", password="test_password")
    response = test_client.get(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == user.id

def test_modify_user(test_client, create_user):
    user = create_user(email="test@example.com", username="test_user", password="test_password")
    modified_data = {"username": "modified_user", "email": "modified@example.com", "password": "modified_password"}
    response = test_client.patch(f"/users/{user.id}", json=modified_data)
    assert response.status_code == 200
    # Validate the modified user details
   
    assert response.json()["email"] == modified_data["email"]
    assert response.json()["username"] == modified_data["username"]
    assert response.json()["password"] == modified_data["password"]

def test_delete_user(test_client, create_user):
    user = create_user(email="test@example.com", username="test_user", password="test_password")

    response = test_client.delete(f"/users/{user.id}")
    assert response.status_code == 204  # Assuming a successful deletion returns a 204 status code

    # Validate that the user is not found after deletion
    response = test_client.get(f"/users/{user.id}")
    assert response.status_code == 404
