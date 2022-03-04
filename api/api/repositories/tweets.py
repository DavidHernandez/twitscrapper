from ..models.tweet import Tweet

class Tweets():

    @staticmethod
    def all():
        return Tweet.objects()

    @staticmethod
    def untagged():
        return Tweets.by_query({'operations.tags': False})

    @staticmethod
    def get(id):
        return Tweet.objects(id=id).first()

    @staticmethod
    def by_author(author_id):
        return Tweets.by_query({'author_id': author_id})

    @staticmethod
    def by_query(query):
        return Tweet.objects(__raw__=query)

    @staticmethod
    def without_extracted_likes():
        return Tweets.by_query({'operations.likes': False, 'liked': {'$gt': 0}})

    @staticmethod
    def without_extracted_retweets():
        return Tweets.by_query({'operations.retweets': False, 'retweeted': {'$gt': 0}})

    @staticmethod
    def without_extracted_replies():
        return Tweets.by_query({'operations.replies': False, 'replies': {'$gt': 0}})

    @staticmethod
    def top_by_account(author_id):
        return Tweets.by_query({'author_id': author_id, 'text': {'$regex': '^(?!RT @).*'}}).order_by('-impact_score')
