from ..config import db


possible_states = {
    'open': 0,
    'in_progress': 1,
    'done': 2,
}

class Task(db.Document):
    operation = db.StringField(primary_key=True)
    group = db.StringField()
    status = db.IntField()

    values = db.DynamicField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.status = 0

    def mark_as(self, status):
        self.status = possible_states[status]

    def complete(self):
        self.status = 2
