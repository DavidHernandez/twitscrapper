from mongoengine.queryset import QuerySet

from ..config import db


class Stat(db.DynamicDocument):
    meta = {'allow_inheritance': True}
    stat_type = db.StringField(required=True)

class TopTagsStat(Stat):
    times = db.IntField()
    tag = db.StringField()
    language = db.StringField()
    user_id = db.IntField()

    def save(self, *args, **kwargs):
        if not self.stat_type:
            self.stat_type = 'top_tags'
        return super(TopTagsStat, self).save(*args, **kwargs)

class TopTopicsStat(Stat):
    times = db.IntField()
    topic = db.StringField()
    language = db.StringField()
    user_id = db.IntField()

    def save(self, *args, **kwargs):
        if not self.stat_type:
            self.stat_type = 'top_topics'
        return super(TopTopicsStat, self).save(*args, **kwargs)

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

class TopMentionsStat(Stat):
    user_id = db.IntField()
    user_handle = db.StringField()
    language = db.StringField()
    mentioned_id = db.IntField()
    mentioned_handle = db.StringField()
    times = db.IntField()

    def save(self, *args, **kwargs):
        if not self.stat_type:
            self.stat_type = 'top_mentions'
        return super(TopMentionsStat, self).save(*args, **kwargs)

class TopHashtagsStat(Stat):
    user_id = db.IntField()
    user_handle = db.StringField()
    language = db.StringField()
    hashtag = db.StringField()
    times = db.IntField()

    def save(self, *args, **kwargs):
        if not self.stat_type:
            self.stat_type = 'top_hashtags'
        return super(TopHashtagsStat, self).save(*args, **kwargs)
