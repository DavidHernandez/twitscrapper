from ..models.tweet import Tweet

class Tweets():

    @staticmethod
    def all():
        return Tweet.objects()
