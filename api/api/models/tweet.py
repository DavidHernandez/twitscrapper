from ..config import db

import re


class Mention(db.EmbeddedDocument):
    id = db.IntField()
    handle = db.StringField()

class Tag(db.EmbeddedDocument):
    topic = db.StringField()
    subtopic = db.StringField()
    tag = db.StringField()
    times = db.IntField()

    def __str__(self):
        return self.tag

    def serialize(self):
        return {
            'topic': self.topic,
            'subtopic': self.subtopic,
            'tag': self.tag,
            'times': self.times
        }

class Tagged(db.EmbeddedDocument):
    knowledgebase = db.StringField()
    public = db.BooleanField()
    topics = db.ListField(db.StringField(), default=list)
    tags = db.EmbeddedDocumentListField(Tag, default=list)

    def __str__(self):
        return self.knowledgebase

    def add_topic(self, topic):
        if topic not in self.topics:
            self.topics.append(topic)

    def add_tag(self, topic, subtopic, tag_name, times):
        if list(filter(lambda tag: tag.tag == tag_name, self.tags)) == []:
            tag = Tag(topic=topic, subtopic=subtopic, tag=tag_name, times=times)
            self.tags.append(tag)
            self.add_topic(topic)

    def remove_single_occurences(self):
        topics_counter = dict()
        for tag in self.tags:
            if tag['topic'] in topics_counter.keys():
                topics_counter[tag['topic']] += tag['times']
            else:
                topics_counter[tag['topic']] = tag['times']
        for key in topics_counter.keys():
            if topics_counter[key] == 1:
                self.tags = list(filter(lambda x: x['topic'] != key, self.tags))
        self.topics = sorted(list(set([tag['topic'] for tag in self.tags])))

    def has_topics(self):
        return len(topics) > 0

    def serialize(self):
        return {
            'knowledgebase': self.knowledgebase,
            'topics': self.topics,
            'tags': list(map(lambda tag_set: tag_set.serialize(), self.tags))
        }

class TweetOperations(db.EmbeddedDocument):
    tags = db.BooleanField(default=False)
    retweets = db.BooleanField(default=False)
    likes = db.BooleanField(default=False)
    quotes = db.BooleanField(default=False)
    replies = db.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags = False
        self.retweets = False
        self.likes = False
        self.quotes = False
        self.replies = False

    def has(self, operation):
        return getattr(self, operation)

    def mark(self, operation):
        setattr(self, operation, True)

    def unmark(self, operation):
        setattr(self, operation, False)

class Tweet(db.Document):
    id = db.IntField(primary_key=True)
    author_id = db.IntField()
    created = db.StringField()
    text = db.StringField()
    language = db.StringField()

    retweeted = db.IntField()
    liked = db.IntField()
    replies = db.IntField()
    quotes = db.IntField()

    tagged = db.EmbeddedDocumentListField(Tagged, default=list)

    hashtags = db.ListField(db.StringField(), default=list)
    mentions = db.EmbeddedDocumentListField(Mention, default=list)
    urls = db.ListField(db.StringField(), default=list)

    raw = db.DynamicField()

    impact_score = db.FloatField()

    operations = db.EmbeddedDocumentField(TweetOperations)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hashtags = []
        self.mentions = []
        self.urls = []
        self.operations = TweetOperations()

    def __str__(self):
        return "{}: {}".format(self.id, self.text)

    def untag(self):
        self.tagged = []
        self.operations.unmark('tags')

    def add_tag(self, kb, is_public, topic, subtopic, tag_name, times):
        tagged = list(filter(lambda tagged: tagged.knowledgebase == kb, self.tagged))

        if len(tagged) > 0:
            tagged = tagged[0]
        else:
            tagged = Tagged(knowledgebase=kb, public=is_public, topics=[], tags=[])
            self.tagged.append(tagged)

        self.operations.mark('tags')
        tagged.add_tag(topic, subtopic, tag_name, times)

    def remove_single_occurences(self):
        for tagged in self.tagged:
            tagged.remove_single_occurences()

    def has_tags(self):
        return any(tagged.has_topics for tagged in self.tagged)

    def add_url(self, url):
        self.urls.append(url)

    def add_hashtag(self, tag):
        self.hashtags.append(tag)

    def add_mention(self, id, handle):
        self.mentions.append(Mention(id=id, handle=handle))

    def calculate_impact_score(self):
        self.impact_score = self.replies * 0.3 + self.quotes * 0.3 + self.retweeted * 0.2 + self.liked * 0.1

    def has(self, operation):
        return self.operations.has(operation)

    @property
    def clean_text(self):
        return self.text.encode('utf-8')
