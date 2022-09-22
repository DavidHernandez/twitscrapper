from ..models.tweet import Tweet

class Tweets():

    @staticmethod
    def all():
        return Tweet.objects().batch_size(100)

    @staticmethod
    def untagged():
        return Tweets.by_query({'operations.tags': False}).batch_size(100)

    @staticmethod
    def tagged():
        return Tweets.by_query({'operations.tags': True}).batch_size(100)

    @staticmethod
    def get(id):
        return Tweet.objects(id=id).first()

    @staticmethod
    def by_author(author_id):
        return Tweets.by_query({'author_id': int(author_id)})

    @staticmethod
    def last(author_id):
        return Tweets.by_author(author_id).order_by('-created').limit(1).first()

    @staticmethod
    def first(author_id):
        return Tweets.by_author(author_id).order_by('created').limit(1).first()

    @staticmethod
    def by_query(query):
        return Tweet.objects(__raw__=query)

    @staticmethod
    def without_extracted_likes():
        return Tweets.by_query({'operations.likes': False, 'liked': {'$gt': 0}, 'text': {'$regex': '^(?!RT @).*'}})

    @staticmethod
    def without_extracted_retweets():
        return Tweets.by_query({'operations.retweets': False, 'retweeted': {'$gt': 0}, 'text': {'$regex': '^(?!RT @).*'}})

    @staticmethod
    def without_extracted_replies():
        return Tweets.by_query({'operations.replies': False, 'replies': {'$gt': 0}})

    @staticmethod
    def top_by_account(author_id):
        return Tweets.by_query({'author_id': author_id, 'text': {'$regex': '^(?!RT @).*'}}).order_by('-impact_score')

    @staticmethod
    def top_liked_from_account(author_id):
        return Tweets.by_query({'author_id': author_id, 'text': {'$regex': '^(?!RT @).*'}}).order_by('-liked')

    @staticmethod
    def top_retweeted_from_account(author_id):
        return Tweets.by_query({'author_id': author_id, 'text': {'$regex': '^(?!RT @).*'}}).order_by('-retweeted')

    @staticmethod
    def top_replied_from_account(author_id):
        return Tweets.by_query({'author_id': author_id, 'text': {'$regex': '^(?!RT @).*'}}).order_by('-replies')
