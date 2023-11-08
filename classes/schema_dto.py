import datetime
import uuid
from pydantic import BaseModel
from typing import Optional


class Task(BaseModel):
    id: str
    title: str
    owner: str
    completed: bool = False

class TaskNoID(BaseModel):
    title: str
    description: Optional[str]   
    owner: str
    completed: bool = False

class User(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    password: str

class UserNoID(BaseModel):
    username: str
    email: str
    password: str

class UserAuth(BaseModel):
    email: str
    password: str