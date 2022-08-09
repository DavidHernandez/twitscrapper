from mongoengine.queryset import QuerySet

from ..config import db


class Stat(db.DynamicDocument):
    meta = {'allow_inheritance': True}
    stat_type = db.StringField(required=True)

class TopFollowersStat(Stat):
    user_id = db.IntField()
    user_handle = db.StringField()
    follower_id = db.IntField()
    follower_handle = db.StringField()
    ranking = db.IntField()
    followers = db.IntField()
    verified = db.BooleanField()
    profession = db.StringField()

    def save(self, *args, **kwargs):
        if not self.stat_type:
            self.stat_type = 'top_followers'
        return super(TopFollowersStat, self).save(*args, **kwargs)
