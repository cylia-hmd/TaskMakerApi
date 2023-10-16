import datetime
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    id: str
    username: str
    password: str  


# Modèle de données Pydantic pour une tâche
class Task(BaseModel):
    id: str
    title: str
    owner: str
    completed: bool = False


class UserNoID(BaseModel):
    username: str
    password: str


class TaskNoID(BaseModel):
    title: str
    description: Optional[str]   
    owner: str
    completed: bool = False