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


task_id_counter = 1

tasks = [
    Task(id="task1", title="medical appointment", owner="Cylia", completed=True),
    Task(id="task2", title="make call", owner="Cylia", completed=False),
    Task(id="task3", title="send email to client", owner="Cylia", completed=False)
]


@router.get('/tasks', response_model=List[Task])
async def get_task(userData: int = Depends(get_current_user)):
    fireBaseObject = db.child("tasks").child(userData['uid']).child('tasks').get(userData['idToken']).val()
    if not fireBaseObject : return []
    resultArray = [value for value in fireBaseObject.values()]
    return resultArray

@router.post('/tasks', status_code=201)
async def create_task(givenTask:TaskNoID, userData: int = Depends(get_current_user)):
    generatedId=uuid.uuid4()
    newTask = Task(id=str(generatedId), title=givenTask.title, description= givenTask.description, owner= givenTask.owner, completed= givenTask.completed)
    # increment_stripe(userData['uid'])
    db.child("tasks").child(userData['uid']).child("tasks").child(str(generatedId)).set(newTask.dict(), token=userData['idToken'])
    return newTask

@router.get('/{task_id}', response_model=Task)
async def get_task_by_ID(task_id: uuid.UUID, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child('tasks').child(userData['uid']).child('tasks').child(str(task_id)).get(userData['idToken']).val()
    if fireBaseobject is not None:
        return fireBaseobject
    raise HTTPException(status_code=404, detail="Task not found")


@router.patch('/{task_id}', status_code=204)
async def modify_task_name(task_id:str, modifiedtask: TaskNoID, userData: int = Depends(get_current_user)):
    fireBaseobject = db.child("tasks").child(userData['uid']).child('tasks').child(task_id).get(userData['idToken']).val()
    if fireBaseobject is not None:
        updatedtask = Task(id=task_id, **modifiedtask.dict())
        return db.child("tasks").child(userData['uid']).child('tasks').child(task_id).update(updatedtask.dict(), userData['idToken'] )
    raise HTTPException(status_code= 404, detail="Task not found")

@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id:str, userData: int = Depends(get_current_user)):
    try:
        fireBaseobject = db.child("tasks").child(userData['uid']).child('tasks').child(task_id).get(userData['idToken']).val()
    except:
        raise HTTPException(
            status_code=403, detail="Unauthaurized"
        )
    if fireBaseobject is not None:
        return db.child("tasks").child(userData['uid']).child('tasks').child(task_id).remove(userData['idToken'])
    raise HTTPException(status_code= 404, detail="Task not found")