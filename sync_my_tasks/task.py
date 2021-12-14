"""Represents a Task
    All dates are UTC
"""

from datetime import datetime

class Task:

    def __init__(
        self, 
        id: int, 
        title: str, 
        description: str, 
        created: datetime = None, 
        completed: datetime = None, 
        due: datetime = None,
        subtasks: 'TaskList' = None
    ) -> None:
        self.task_id = id
        self.task_title = title
        self.task_description = description
        self.task_created = created
        self.task_completed = completed
        self.task_due = due
        self.task_subtasks = subtasks
