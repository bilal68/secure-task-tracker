from sqlalchemy.orm import Session
from app.db.models import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(db: Session, user_id: int, task_in: TaskCreate) -> Task:
    task = Task(
        user_id=user_id, **task_in.model_dump(exclude_unset=True, exclude_none=True)
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_tasks(
    db: Session, user_id: int = None, skip: int = 0, limit: int = 50
) -> list[Task]:
    query = db.query(Task)
    if user_id is not None:
        query = query.filter(Task.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_task_for_owner(db: Session, user_id: int, task_id: int) -> Task | None:
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()


def update_task(db: Session, task: Task, task_in: TaskUpdate) -> Task:
    for k, v in task_in.model_dump(exclude_unset=True).items():
        setattr(task, k, v)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()
