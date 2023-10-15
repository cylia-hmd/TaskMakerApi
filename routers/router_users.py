from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models  # Assurez-vous que le module "models" contient vos classes SQLAlchemy
from . import database  # Module contenant la configuration de la base de données

user_router = APIRouter()

# Endpoint pour créer un utilisateur
@app.post("/users/", response_model=User)
def create_user(user: User):
    users_db.append(user)
    return user

# Endpoint pour récupérer un utilisateur par son nom d'utilisateur
@app.get("/users/{username}", response_model=User)
def get_user(username: str):
    user = next((user for user in users_db if user.username == username), None)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user

# Endpoint pour récupérer la liste de tous les utilisateurs
@app.get("/users/", response_model=List[User])
def get_all_users():
    return users_db