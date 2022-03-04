import uuid

from ..models.task import Task

def create_group_task(operation, values):
    group = uuid.uuid1()

    for value in values:
        task = Task(operation=operation, group=group, value=value)
        task.save()
