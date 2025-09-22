# app/core/enums.py
from enum import Enum

class StatusEnum(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
