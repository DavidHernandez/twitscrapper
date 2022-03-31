from ..config import db
from datetime import datetime, timedelta

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

class Date(db.EmbeddedDocument): 
    year = db.IntField()
    month = db.IntField()
    day = db.IntField()
    hour = db.IntField()
    minute = db.IntField()
    day_of_week = db.IntField()


    @staticmethod
    def from_iso_8061(iso_date):
        format = '%Y-%m-%dT%H:%M:%S.000Z'
        parsed_date = datetime.strptime(iso_date, format)
        #fix timezone
        parsed_date += timedelta(hours=1)

        date = Date(
                    year=parsed_date.year,
                    month=parsed_date.month,
                    day=parsed_date.day,
                    hour=parsed_date.hour,
                    minute=parsed_date.minute,
                    day_of_week=parsed_date.weekday()
                )
        return date

    @property
    def weekday(self):
        daymap = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        return daymap[self.day_of_week]



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
        return len(self.topics) > 0

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

    retweeters = db.ListField(db.IntField(), default=list)
    like_list = db.ListField(db.IntField(), default=list)
    reply_list = db.ListField(db.IntField(), default=list)

    tagged = db.EmbeddedDocumentListField(Tagged, default=list)

    hashtags = db.ListField(db.StringField(), default=list)
    mentions = db.EmbeddedDocumentListField(Mention, default=list)
    urls = db.ListField(db.StringField(), default=list)

    raw = db.DynamicField()

    impact_score = db.FloatField()

    operations = db.EmbeddedDocumentField(TweetOperations)
    created_date = db.EmbeddedDocumentField(Date)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "{}: {}".format(self.id, self.text)

    def calculate_impact_score(self):
        self.impact_score = self.replies * 0.3 + self.quotes * 0.3 + self.retweeted * 0.2 + self.liked * 0.1

    def has_tags(self):
        return any(tagged.has_topics for tagged in self.tagged)

    def add_tag(self, kb, is_public, topic, subtopic, tag_name, times):
        tagged = list(filter(lambda tagged: tagged.knowledgebase == kb, self.tagged))

        if len(tagged) > 0:
            tagged = tagged[0]
        else:
            tagged = Tagged(knowledgebase=kb, public=is_public, topics=[], tags=[])
            self.tagged.append(tagged)

        self.operations.mark('tags')
        tagged.add_tag(topic, subtopic, tag_name, times)

    def untag(self):
        self.tagged = []
        self.operations.unmark('tags')

    def remove_single_occurences(self):
        for tagged in self.tagged:
            tagged.remove_single_occurences()

    def add_url(self, url):
        self.urls.append(url)

    def add_hashtag(self, tag):
        self.hashtags.append(tag)

    def add_mention(self, id, handle):
        self.mentions.append(Mention(id=id, handle=handle))

    def add_like(self, user_id):
        self.mark('likes')
        if user_id not in self.like_list:
            self.like_list.append(user_id)

    def add_retweeter(self, user_id):
        self.mark('retweets')
        if user_id not in self.retweeters:
            self.retweeters.append(user_id)

    def add_reply(self, tweet_id):
        self.mark('replies')
        if tweet_id not in self.reply_list:
            self.reply_list.append(tweet_id)

    def has(self, operation):
        return self.operations.has(operation)

    def mark(self, operation):
        return self.operations.mark(operation)

    def unmark(self, operation):
        return self.operations.unmark(operation)

    @property
    def clean_text(self):
        return self.text.encode('utf-8')

    @staticmethod
    def from_json(json):
        metrics = json['public_metrics']

        tweet = Tweet(
            id=json['id'],
            author_id=json['author_id'],
            created=json['created_at'],
            text=json['text'],

            retweeted=metrics['retweet_count'],
            liked=metrics['like_count'],
            replies=metrics['reply_count'],
            quotes=metrics['quote_count'],

            language=json['lang'],

            raw=json
        )

        if 'entities' in json:
            entities = json['entities']
            if 'hashtags' in entities:
                for hashtag in entities['hashtags']:
                    tweet.add_hashtag(hashtag['tag'])

            if 'urls' in entities:
                for url in entities['urls']:
                    tweet.add_url(url['expanded_url'])

            if 'mentions' in entities:
                for mention in entities['mentions']:
                    tweet.add_mention(mention['id'], mention['username'])

        tweet.calculate_impact_score()
        tweet.parse_date()
        tweet.save()

        return tweet

    def parse_date(self):
        self.created_date = Date.from_iso_8061(self.created)

    def to_json(self):
        return self.raw
