import hashlib
from ..config import db
from datetime import datetime

class Operation(db.Document):
    id = db.StringField(db_field='_id', primary_key=True)
    command = db.StringField()
    parameters = db.ListField(db.StringField(), default=list)
    execution_date = db.IntField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = Operation.hash_id(self.command, self.parameters)

        return super(Operation, self).save(*args, **kwargs)

    def complete(self):
        date = datetime.now()
        self.execution_date = str(date.year) + str(date.month).zfill(2)
        self.save()

    @staticmethod
    def hash_id(command, parameters):
        return generate_id(command, str(parameters))

def generate_id(*args):
    try:
        return hashlib.sha1(
            u''.join(args).encode('utf-8')
        ).hexdigest()
    except Exception:
        return 'ID_ERROR'
