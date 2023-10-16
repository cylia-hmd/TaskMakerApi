import datetime
from pydantic import BaseModel


# Modèle de données Pydantic pour un utilisateur
class User(BaseModel):
    username: str
    password: str

# Modèle de données Pydantic pour une tâche
class Task(BaseModel):
    title: str
    description: str
    due_date: str
    completed: bool = False
    owner: str
