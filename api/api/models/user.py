from ..config import db


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
        return len(self.topics) > 0

    def serialize(self):
        return {
            'knowledgebase': self.knowledgebase,
            'topics': self.topics,
            'tags': list(map(lambda tag_set: tag_set.serialize(), self.tags))
        }

class UserOperations(db.EmbeddedDocument):
    mentions = db.BooleanField(default=False)
    tweets = db.BooleanField(default=False)
    followers = db.BooleanField(default=False)
    following = db.BooleanField(default=False)
    lists = db.BooleanField(default=False)
    profession = db.BooleanField(default=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def has(self, operation):
        return getattr(self, operation)

    def mark(self, operation):
        setattr(self, operation, True)

    def unmark(self, operation):
        setattr(self, operation, False)

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

    follower_list = db.ListField(db.IntField(), default=list)
    mention_list = db.ListField(db.IntField(), default=list)
    membership_list = db.ListField(db.IntField(), default=list)

    tagged = db.EmbeddedDocumentListField(Tagged, default=list)

    operations = db.EmbeddedDocumentField(UserOperations)

    def save(self, *args, **kwargs):
        if self.operations is None:
            self.operations = UserOperations()

        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return "@{}".format(self.name)

    def add_follower(self, user_id):
        self.mark('followers')
        self.follower_list.append(user_id)

    def add_mentions(self, tweet_id):
        self.mark('mentions')
        self.mention_list.append(tweet_id)

    def add_membership(self, list_id):
        self.mark('lists')
        self.membership_listt.append(list_id)

    def add(self, field, value):
        setattr(self, field, value)

    def has_tags(self):
        return any(tagged.has_topics for tagged in self.tagged)

    def add_tag(self, kb, is_public, topic, subtopic, tag_name, times):
        tagged = list(filter(lambda tagged: tagged.knowledgebase == kb, self.tagged))

        if len(tagged) > 0:
            tagged = tagged[0]
        else:
            tagged = Tagged(knowledgebase=kb, public=is_public, topics=[], tags=[])
            self.tagged.append(tagged)

        self.operations.mark('profession')
        tagged.add_tag(topic, subtopic, tag_name, times)

    def untag(self):
        self.tagged = []
        self.operations.unmark('profession')

    def has(self, operation):
        return self.operations.has(operation)

    def mark(self, operation):
        return self.operations.mark(operation)

    def unmark(self, operation):
        return self.operations.unmark(operation)

    @property
    def profession(self):
        if not self.has_tags():
            return ''
        profession = None
        professions = self.tagged[0]

        if not len(professions.tags):
            return ''

        for tag in professions.tags:
            if not profession:
                profession = tag
            if profession.times < tag.times:
                profession = tag

        return profession.subtopic


    @staticmethod
    def from_json(json):
        metrics = json['public_metrics']
        user = User(
            id=json['id'],
            handle=json['username'].lower(),
            name=json['name'],
            followers=metrics['followers_count'],
            following=metrics['following_count'],
            tweets=metrics['tweet_count'],
            profile_pic=json['profile_image_url'],
            description=json['description'],
            url=json['url'],
            created_at=json['created_at'],
            verified=json['verified'],
        )

        if 'location' in json:
            user.location = json['location']

        user.save()
        return user
