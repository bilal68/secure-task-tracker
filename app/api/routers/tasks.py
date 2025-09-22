from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.db.models import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskOut
from app.crud import task_crud

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return task_crud.create_task(db, current_user.id, task_in)


@router.get("/", response_model=List[TaskOut])
def list_tasks(
    skip: int = 0,
    limit: int = 500,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        # Admin: get all tasks
        return task_crud.get_tasks(db, user_id=None, skip=skip, limit=limit)
    else:
        # Regular user: get only their own tasks
        return task_crud.get_tasks(db, current_user.id, skip, limit)


@router.get("/{task_id}", response_model=TaskOut)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_crud.get_task_for_owner(db, current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_crud.get_task_for_owner(db, current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_crud.update_task(db, task, task_in)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    task = task_crud.get_task_for_owner(db, current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_crud.delete_task(db, task)
    return
