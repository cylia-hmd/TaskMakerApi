from fastapi import APIRouter, HTTPException
from typing import List,Optional
import uuid
from classes.schema_dto import Task, TaskNoID

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
async def get_tasks():
    return tasks

@router.post('/', response_model=Task, status_code=201)
async def create_task(givenTitle: TaskNoID, givenOwner= str, Ifcompleted=bool ):
    generatedId=uuid.uuid4()
    newTask= Session(id=str(generatedId), title=givenTitle, owner=givenOwner, completed = bool  )
    sessions.append(newTask)
    return newTask

@router.get('/{task_id}', response_model=Task)
async def get_task_by_id(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch('/{task_id}', status_code=204)
async def modify_task_title(task_id: int, modified_task: Task):
    for task in tasks:
        if task.id == task_id:
            task.title = modified_task.title
            return
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail="Task not found")
