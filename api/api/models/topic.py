from mongoengine.queryset import QuerySet
from natsort import natsorted, ns

from ..config import db


class TopicQuerySet(QuerySet):

    def natsorted(self):
        return natsorted(
                self,
                key=lambda x: x.name,
                alg=ns.IGNORECASE)


class Tag(db.EmbeddedDocument):
    tag = db.StringField()
    subtopic = db.StringField()
    regex = db.StringField()
    shuffle = db.BooleanField()

    def __str__(self):
        return self.tag


class Topic(db.Document):
    id = db.StringField(db_field='_id', primary_key=True)
    name = db.StringField()
    shortname = db.StringField()
    description = db.ListField(db.StringField())
    tags = db.EmbeddedDocumentListField(Tag)
    knowledgebase = db.StringField()
    public = db.BooleanField()

    meta = {
            'collection': 'topics',
            'ordering': ['name'],
            'indexes': ['name'],
            'queryset_class': TopicQuerySet
            }

    def __str__(self):
        return self.name

    def add_tag(self, data):
        tag = Tag(
                tag=data['tag'],
                subtopic=data['subtopic'],
                regex=data['regex'],
                shuffle=data['shuffle']
            )
        self.tags.append(tag)
        return tag

    @staticmethod
    def from_json(data):
        topic = Topic(
                id=data['_id'],
                name=data['name'],
                shortname=data['shortname'],
                description=data['description'],
                knowledgebase=data['knowledgebase']
            )
        for tag in data['tags']:
            topic.add_tag(tag)
        topic.save()
        return topic
