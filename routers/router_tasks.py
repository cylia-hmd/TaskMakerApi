from fastapi import APIRouter, HTTPException
from typing import List
from classes.schema_dto import Task, TaskNoID

router = APIRouter(
    prefix='/tasks',
    tags=["Tasks"]
)

tasks = [
    Task(id=str(uuid.uuid4()), title="Task 1", owner="user1"),
    Task(id=str(uuid.uuid4()), title="Task 2", owner="user2"),
    Task(id=str(uuid.uuid4()), title="Task 3", owner="user1")
]

@router.get('/', response_model=List[Task])
async def get_tasks():
    return tasks

@router.post('/', response_model=Task, status_code=201)
async def create_task(task: TaskNoID):
    new_task = Task(id=str(uuid.uuid4()), title=task.title, owner=task.owner)
    tasks.append(new_task)
    return new_task

@router.get('/{task_id}', response_model=Task)
async def get_task_by_id(task_id: str):
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@router.patch('/{task_id}', status_code=204)
async def modify_task_title(task_id: str, modified_task: TaskNoID):
    for task in tasks:
        if task.id == task_id:
            task.title = modified_task.title
            return
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete('/{task_id}', status_code=204)
async def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail="Task not found")
