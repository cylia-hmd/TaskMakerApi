from fastapi import APIRouter, HTTPException
from typing import List
import uuid
from classes.schema_dto import User, UserNoID

router_user = APIRouter(
    prefix='/users',
    tags=["Users"]
)

users = [
    User(id=str(uuid.uuid4()), username="user1"),
    User(id=str(uuid.uuid4()), username="user2"),
    User(id=str(uuid.uuid4()), username="user3")
]

@router_user.get('/', response_model=List[User])
async def get_users():
    return users

@router_user.post('/', response_model=User, status_code=201)
async def create_user(user: UserNoID):
    new_user = User(id=str(uuid.uuid4()), username=user.username)
    users.append(new_user)
    return new_user

@router_user.get('/{user_id}', response_model=User)
async def get_user_by_id(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router_user.patch('/{user_id}', status_code=204)
async def modify_user_name(user_id: str, modified_user: UserNoID):
    for user in users:
        if user.id == user_id:
            user.username = modified_user.username
            return
    raise HTTPException(status_code=404, detail="User not found")

@router_user.delete('/{user_id}', status_code=204)
async def delete_user(user_id: str):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return
    raise HTTPException(status_code=404, detail="User not found")
