from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
import uuid
from classes.schema_dto import Task, TaskNoID
from database.firebase import db
from routers.router_auth import get_current_user


router = APIRouter(
    prefix='/tasks',
    tags=["Tasks"]
)

# Utilisez une variable globale pour suivre les identifiants des tâches
task_id_counter = 1

tasks = [
    Task(id="task1", title="medical appointment", owner="Cylia", completed=True),
    Task(id="task2", title="make call", owner="Cylia", completed=False),
    Task(id="task3", title="send email to client", owner="Cylia", completed=False)
]


@router.get('/', response_model=List[Task])
async def get_sessions(userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('task').get(userData['idToken']).val()
    resultArray = [value for value in fireBaseobject.values()]
    return resultArray

@router.post('/', response_model=Task, status_code=201)
async def create_sessions(givenName:TaskNoID, userData: int = Depends(get_current_user)):
    generatedId=uuid.uuid4()
    newTask= Task(id=str(generatedId), title=givenTitle, owner=givenOwner, completed = bool )
    db.child("users").child(userData['uid']).child("task").child(str(generatedId)).set(newTask.model_dump())
    return newTask

@router.get('/{task_id}', response_model=Task)
async def get_task_by_id(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@router.patch('/{task_id}', status_code=204)
async def modify_student_name(task_id:int, modified_task: Task, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("users").child(userData['uid']).child('tasks').child(task_id).get(userData['idToken']).val()
    if fireBaseobject is not None:
        updatedTask = Task(id=task_id, **modifiedTask.model_dump())
        return db.child("users").child(userData['uid']).child('tasks').child(task_id).update(updatedTask.model_dump(), userData['idToken'] )
    raise HTTPException(status_code= 404, detail="Session not found")




@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: int, userData: int = Depends(get_current_user)):
    try:
        fireBaseobject = db.child("users").child(userData['uid']).child('tasks').child(task_id).get(userData['idToken']).val()
    except:
        raise HTTPException(
            status_code=403, detail="Accès interdit"
        )
    if fireBaseobject is not None:
        return db.child("users").child(userData['uid']).child('tasks').child(task_id).remove(userData['idToken'])
    raise HTTPException(status_code= 404, detail="Session not found")