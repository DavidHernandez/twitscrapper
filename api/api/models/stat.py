from ..config import db

class Stat(db.Document):
    id = db.StringField(primary_key=True)
    year = db.IntField()
    month = db.IntField()
    day = db.IntField()
    period = db.StringField()
    handle = db.StringField()
    tweets = db.IntField()
    likes = db.IntField()
    retweets = db.IntField()
    mentions = db.DictField()
    hashtags = db.DictField()
    topics = db.DictField()
    subtopics = db.DictField()
    tags = db.DictField()
    langs = db.DictField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tweets = 0
        self.likes = 0
        self.retweets = 0

    def add_likes(self, likes):
            self.likes += likes

    def increment_tweets(self):
            self.tweets = self.tweets + 1

    def add_retweets(self, retweets):
            self.retweets += retweets

    def add_tag(self, tag):
        key = self.clean_dict_keys(tag['topic'])
        if key in self.topics:
            self.topics[key] += tag['times']
        else:
            self.topics[key] = tag['times']

        key = self.clean_dict_keys(tag['subtopic'])
        if key in self.subtopics:
            self.subtopics[key] += tag['times']
        else:
            self.subtopics[key] = tag['times']

        key = self.clean_dict_keys(tag['tag'])
        if key in self.tags:
            self.tags[key] += tag['times']
        else:
            self.tags[key] = tag['times']

    def add_hashtag(self, hashtag):
        if hashtag in self.hashtags:
            self.hashtags[hashtag] += 1
        else:
            self.hashtags[hashtag] = 1

    def add_mention(self, mention):
        if mention in self.mentions:
            self.mentions[mention] += 1
        else:
            self.mentions[mention] = 1

    def add_lang(self, lang):
        if lang in self.langs:
            self.langs[lang] += 1
        else:
            self.langs[lang] = 1

    def clean_dict_keys(self, key):
        return key.replace('.', '-')
