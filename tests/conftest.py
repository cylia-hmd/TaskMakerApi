from fastapi.testclient import TestClient
from main import app
import pytest


# from database.firebase import authUser


import os
os.environ['TESTING'] = 'True'


client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    
    def remove_test_data():
       
        pass

    request.addfinalizer(remove_test_data)


@pytest.fixture
def create_user():
    user_data = {
        "email": "test.user2@gmail.com",
        "password": "password",
        
    }
    user_credential = client.post("/auth/signup", json=user_data)
    return user_data


@pytest.fixture
def auth_user(create_user):
    user_data = {
        "username": create_user["email"],
        "password": create_user["password"],
        
    }
    user_credential = client.post("/auth/login", data=user_data)
    return user_credential.json()