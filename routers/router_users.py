from fastapi import APIRouter, HTTPException, Depends
from typing import List
from classes.schema_dto import User, UserNoID
import uuid
from database.firebase import db
from routers.router_auth import get_current_user

router= APIRouter(
    prefix='/users',
    tags=["Users"]
)

users = [
    User(id=uuid.uuid4(), username="cylia", email="cy@gmail.com", password="6025"),
    User(id=uuid.uuid4(), username="luna", email="lune@gmail.com", password="12345"),
    User(id=uuid.uuid4(), username="kay", email="kay@gmail.com", password="kay")
]

@router.get('/', response_model=List[User])
async def get_user(userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('users').get(userData['idToken']).val()
    if not fireBaseobject : return []
    resultArray = [value for value in fireBaseobject.values()]
    return resultArray

@router.post('/', response_model=User, status_code=201)
async def create_user(givenUsername: UserNoID, userData: int = Depends(get_current_user)):
    generatedId = uuid.uuid4()
    newUser = User(id=generatedId, username=givenUsername.username, email=givenUsername.email, password=givenUsername.password)  
    user_dict = {
        "id": str(newUser.id),
        "username": newUser.username,
        "email": newUser.email,
        "password": newUser.password
    }
    db.child("users").child(userData['uid']).child("users").child(generatedId).set(user_dict, token=userData['idToken'])  # Enregistrez l'utilisateur dans la base de données
    return newUser

@router.get('/{user_id}', response_model=User)
async def get_user_by_ID(user_id: uuid.UUID, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child('users').child(userData['uid']).child('users').child(str(user_id)).get(userData['idToken']).val()
    if fireBaseobject is not None:
        return fireBaseobject
    raise HTTPException(status_code=404, detail="User not found")

@router.patch('/{user_id}', status_code=204)
async def modify_user_title(user_id: uuid.UUID, modifiedUser: UserNoID, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child('users').child(userData['uid']).child('users').child(user_id).get(userData['idToken']).val()
    if fireBaseobject is not None:
        user_dict = {
            "username": modifiedUser.username,
            "email": modifiedUser.email,
            "password": modifiedUser.password
        }
        db.child('users').child(userData['uid']).child('users').child(user_id).update(user_dict, token=userData['idToken'])
        return
    raise HTTPException(status_code=404, detail="User not found")

@router.delete('/{user_id}', status_code=204)
async def delete_user(user_id: uuid.UUID, userData: int = Depends(get_current_user)):  # Change data type to uuid.UUID
    try: 
        fireBaseobject = db.child('users').child(userData['uid']).child('users').child(user_id).get(userData['idToken']).val()
    except:
        raise HTTPException(
            status_code=403,
            detail = "Accés interdit"
        )
    if fireBaseobject is not None:
        db.child('users').child(userData['uid']).child('users').child(user_id).remove(token=userData['idToken'])
        return
    raise HTTPException(status_code=404, detail="User not found")