from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models  # Assurez-vous que le module "models" contient vos classes SQLAlchemy
from . import database  # Module contenant la configuration de la base de données

task_router = APIRouter()

# Endpoint pour créer une tâche
@app.post("/tasks/", response_model=Task)
def create_task(task: Task):
    tasks_db.append(task)
    return task

# Endpoint pour récupérer toutes les tâches de l'utilisateur actuel
@app.get("/tasks/", response_model=List[Task])
def get_tasks(current_user: User = Depends()):
    user_tasks = [task for task in tasks_db if task.owner == current_user.username]
    return user_tasks

# Endpoint pour mettre à jour une tâche par son ID
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task, current_user: User = Depends()):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    existing_task = tasks_db[task_id]
    if existing_task.owner != current_user.username:
        raise HTTPException(status_code=403, detail="Permission refusée")
    tasks_db[task_id] = task
    return task

# Endpoint pour supprimer une tâche par son ID
@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, current_user: User = Depends()):
    if task_id < 0 or task_id >= len(tasks_db):
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    existing_task = tasks_db[task_id]
    if existing_task.owner != current_user.username:
        raise HTTPException(status_code=403, detail="Permission refusée")
    deleted_task = tasks_db.pop(task_id)
    return deleted_task
