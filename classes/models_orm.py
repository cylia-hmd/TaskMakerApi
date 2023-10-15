from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Créez une instance de la classe de base pour créer les modèles
Base = declarative_base()


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
