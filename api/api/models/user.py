from ..config import db


class UserOperations(db.EmbeddedDocument):
    mentions = db.BooleanField(default=False)
    followers = db.BooleanField(default=False)
    following = db.BooleanField(default=False)
    lists = db.BooleanField(default=False)
    profession = db.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mentions = False
        self.followers = False
        self.following = False
        self.lists = False
        self.profession = False

class User(db.Document):
    id = db.IntField(db_field='id', primary_key=True)
    name = db.StringField()
    handle = db.StringField()
    followers = db.IntField()
    following = db.IntField()
    tweets = db.IntField()
    profile_pic = db.StringField()
    description = db.StringField()
    location = db.StringField()
    created_at = db.DateTimeField()
    url = db.StringField()
    verified = db.BooleanField()
    profession = db.StringField()

    operations = db.EmbeddedDocumentField(UserOperations)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.operations = UserOperations()

    def __str__(self):
        return "@{}".format(self.name)

    def add(self, field, value):
        setattr(self, field, value)
