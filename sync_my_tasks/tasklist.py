"""Represents a named list of Tasks
"""
from sync_my_tasks.task import Task

class TaskList:

    def __init__(self, name):
        self.task_list:list[Task] = []
        self.name = name

    def add(self, task: Task) -> None:
        self.task_list.append(task)
