from fastapi import APIRouter, HTTPException
from typing import List, Optional
import uuid
from classes.schema_dto import User, UserNoID

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

users = [
    User(id="user1", username="Cylia", password="1232"),
    User(id="user2", username="Yuna", password="1230"),
    User(id="user3", username="Youva", password="mule")
]

@router.get('/', response_model=List[User])
async def get_users():
    return users

@router.post('/', response_model=User, status_code=201)
async def create_user(givenName: str, givenPassword: str):

    generatedId=uuid.uuid4()
    # Créez une instance de la classe User en fournissant une valeur pour le champ password
    newUser = User(id=str(generatedId), username=givenName, password= givenPassword)
    users.append(newUser)
    # Faites ce dont vous avez besoin avec l'instance user
    return newUser

@router.get('/{user_id}', response_model=User)
async def get_user_by_id(user_id: str):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.patch('/{user_id}', status_code=204)
async def modify_user_name(user_id: str, modifiedUser: UserNoID):
    for user in users:
        if user.id == user_id:
            user.username = modifiedUser.username
            return
    raise HTTPException(status_code=404, detail="User not found")

@router.delete('/{user_id}', status_code=204)
async def delete_user(user_id: str):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return
    raise HTTPException(status_code=404, detail="User not found")
