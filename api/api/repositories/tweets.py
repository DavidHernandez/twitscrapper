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
    def by_query(query):
        return Tweet.objects(__raw__=query)

