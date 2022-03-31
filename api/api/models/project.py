import uuid
from datetime import datetime
from ..config import db

NEW_STATE = 0
DOING_STATE = 1
DEPENDENCIES = 2
DONE_STATE = 3

class Task(db.EmbeddedDocument):
    meta = {'allow_inheritance': True}

class Subtask(Task):
    operation = db.StringField()
    name = db.StringField()
    status = db.IntField(default=NEW_STATE)
    tasks = db.EmbeddedDocumentListField(Task, default=list)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())
    operations = db.ListField(db.StringField(), default=list)

    values = db.DynamicField()

    def start(self):
        self.update_date()
        self.status = DOING_STATE

    def complete(self):
        self.update_date()
        self.status = DONE_STATE

    def start_dependants(self):
        self.status = DEPENDENCIES

    def is_new(self):
        return self.status == NEW_STATE

    def is_doing(self):
        return self.status == DOING_STATE

    def is_on_dependants(self):
        return self.status == DEPENDENCIES

    def is_done(self):
        return self.status == DONE_STATE

    def has_completed_operations(self):
        return len(self.operations) == 0

    def has_dependants(self):
        return len(self.tasks) > 0

    def get_new_tasks(self):
        return filter(lambda task: task.is_new(), self.tasks)

    def get_active_tasks(self):
        return filter(lambda task: task.is_doing(), self.tasks)

    def get_tasks_on_dependants(self):
        return filter(lambda task: task.is_on_dependants(), self.tasks)

    def add_operations(self, operation_ids):
        self.operations.extend(operation_ids)
        self.operations = list(set(self.operations))

    def update_date(self):
        self.updated_at = default=datetime.now()

    def add_task(self, task_name, operation, subtasks=None):
        new_task = Subtask(name=task_name, operation=operation)
        if subtasks:
            for task in subtasks:
                dependencies = None
                if 'child_tasks' in task:
                    dependencies = task['child_tasks']
                new_task.add_task(task['name'], operation=task['command'], subtasks=dependencies)
        self.tasks.append(new_task)

class Project(db.Document):
    id = db.StringField(db_field='_id', primary_key=True)
    type = db.StringField()
    status = db.IntField(default=NEW_STATE)
    data = db.DynamicField()
    tasks = db.EmbeddedDocumentListField(Task, default=list)
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())

    def save(self, *args, **kwargs):
        if not self.id:
            id = uuid.uuid1()
            self.id = str(id)

        if not self.status:
            self.status = NEW_STATE

        self.update_date()
        return super(Project, self).save(*args, **kwargs)

    def start(self):
        for task in self.tasks:
            task.start()

        self.status = DOING_STATE

    def complete(self):
        self.status = DONE_STATE

    def is_new(self):
        return self.status == NEW_STATE

    def is_doing(self):
        return self.status == DOING_STATE

    def is_done(self):
        return self.status == DONE_STATE

    def get_new_tasks(self):
        return filter(lambda task: task.is_new(), self.tasks)

    def get_active_tasks(self):
        return filter(lambda task: task.is_doing(), self.tasks)

    def get_tasks_on_dependants(self):
        return filter(lambda task: task.is_on_dependants(), self.tasks)

    def update_date(self):
        self.updated_at = default=datetime.now()

    def tasks_are_completed(self):
        all_finished = True
        for task in self.tasks:
            all_finished = all_finished and task.is_done()
        return all_finished

    def add_task(self, task_name, operation, subtasks=None):
        new_task = Subtask(name=task_name, operation=operation)
        if subtasks:
            for task in subtasks:
                dependencies = None
                if 'child_tasks' in task:
                    dependencies = task['child_tasks']
                new_task.add_task(task['name'], operation=task['command'], subtasks=dependencies)
        self.tasks.append(new_task)
