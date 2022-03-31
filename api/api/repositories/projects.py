from ..models.project import Project, NEW_STATE, DONE_STATE

class Projects():

    @staticmethod
    def by_query(query):
        return Project.objects(__raw__=query)

    @staticmethod
    def get(project_id):
        return Project.objects(id=project_id).first()

    @staticmethod
    def active():
        return Project.objects(status__lt=DONE_STATE)
