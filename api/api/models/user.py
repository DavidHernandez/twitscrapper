from ..config import db


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

    def __str__(self):
        return "@{}".format(self.name)

    def add(self, field, value):
        setattr(self, field, value)
