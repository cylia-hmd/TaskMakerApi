from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from . import users, tasks  # Importez les fichiers de routeurs

app = FastAPI()



# Stockage en mémoire pour les utilisateurs et les tâches
users_db = []
tasks_db = []




# Inclure le routeur pour les utilisateurs
app.include_router(users.user_router, prefix="/users", tags=["users"])

# Inclure le routeur pour les tâches
app.include_router(tasks.task_router, prefix="/tasks", tags=["tasks"])