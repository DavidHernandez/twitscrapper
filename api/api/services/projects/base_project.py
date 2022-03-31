from ...models.operation import Operation
from ...models.project import Project
from ...repositories.operations import Operations
from ...repositories.projects import Projects
from datetime import datetime

class BaseProject():

    def __init__(self, project):
        self.project = project

    @staticmethod
    def from_id(project_id):
        project = Projects.get(project_id)

        return BaseProject(project)

    def update_status(self, operations):
        if self.project.is_new():
            print(f'Project has started')
            self.start(self.project)
        elif self.project.is_doing():
            print(f'Project is in progress')
            self.update_tasks(self.project, operations)
            if self.project.tasks_are_completed():
                print('Project completed')
                self.project.complete()

        print(f'Saving project')
        self.project.save()

    def start(self, current_task):
        self.start_tasks(current_task)

        current_task.start()

    def update_tasks(self, current_task, operations):
        print(f'|-Updating task status')
        for task in current_task.tasks:
            self.update_task_status(task, operations)

    def update_task_status(self, task, operations):
        if task.is_new():
            print(f'  |-Task {task.name} is new, starting')
            self.start(task)
        elif task.is_doing():
            print(f'  |-Task {task.name} is in progress, updating')
            self.update_operations(task)
            if task.has_completed_operations():
                print(f'    |-Task {task.name} has completed operations')
                if task.has_dependants():
                    print(f'      |-Task {task.name} has dependants, starting tasks and updating status')
                    self.start_tasks(task)
                    task.start_dependants()
                else:
                    print(f'      |-Task {task.name} has no dependants, marking as complete')
                    task.complete()
        elif task.is_on_dependants():
            print(f'  |-Task {task.name} is on dependants, updating childrens')
            self.update_operations(task)
            all_completed = True
            for subtask in task.tasks:
                self.update_task_status(subtask, operations)
                all_completed = all_completed and subtask.is_done()
            if all_completed:
                print(f'    |-All dependendants are completed, completing task {task.name}')
                task.complete()

    def update_operations(self, task):
        operations = task.operations
        unfinished_operations = Operations.get_unfinished(operations)
        updated_operations = []
        for operation in unfinished_operations:
            updated_operations.append(operation.id)
        task.operations = updated_operations

    def start_tasks(self, task):
        new_tasks = task.get_new_tasks()
        for subtask in new_tasks:
            print(f'        |-Adding operations for task {subtask.name}')
            self.create_task_operations(subtask)
            subtask.start()

    def create_task_operations(self, task):
        name = task.name
        operation = task.operation

        parameters_function = name + '_parameters'
        operation_function = name + '_operation'

        parameters = getattr(self, parameters_function)()

        operation_ids = getattr(self, operation_function)(operation, parameters)
        task.add_operations(operation_ids)

    def create_standard_operation(self, command, parameters):
        hash_id = Operation.hash_id(command, parameters)
        operation = Operations.get(hash_id)

        if not operation:
            Operation(command=command, parameters=parameters).save()
            return [hash_id]

        date = datetime.now()
        current_date = str(date.year) + str(date.month).zfill(2)

        return [hash_id]

    def create_standard_multioperation(self, command, parameters):
        ids = []
        for item in parameters:
            ids.extend(self.create_standard_operation(command, [item]))
        return ids
        
    def add_tasks(self):
        tasks = self.get_project_tasks() 

        for task in tasks:
            self.project.add_task(task['name'], task['command'], task['child_tasks'])
        self.project.save()

    def get_project_tasks(self):
        return []

