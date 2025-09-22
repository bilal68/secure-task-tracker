from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.core.enums import StatusEnum

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: StatusEnum = StatusEnum.todo

class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusEnum] = None


class TaskOut(TaskBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
