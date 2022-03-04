from ..config import config
from twarc.client2 import Twarc2
from twarc import Twarc


class Twitter():
    def __init__(self, *args, **kwargs):
        self.v2 = Twarc2(
            config.TWITTER_CONSUMER_KEY,
            config.TWITTER_CONSUMER_SECRET,
            config.TWITTER_TOKEN,
            config.TWITTER_TOKEN_SECRET
        )

        self.v1 = Twarc(
            config.TWITTER_CONSUMER_KEY,
            config.TWITTER_CONSUMER_SECRET,
            config.TWITTER_TOKEN,
            config.TWITTER_TOKEN_SECRET
        )

    def timeline(self, user_id):
        return self.v2.timeline(user_id)

    def mentions(self, user_id):
        return self.v2.mentions(user_id)

    def user_lookup(self, users):
        return self.v2.user_lookup(users, usernames=True)

    def followers(self, user_id):
        return self.v2.followers(user_id)

    def retweeted_by(self, tweet_id):
        return self.v2.retweeted_by(tweet_id)

    def liking_users(self, tweet_id):
        return self.v2.liking_users(tweet_id)

    def replies(self, conversation_id):
        return self.v2.search_recent('conversation_id:' + conversation_id)


twitter = Twitter()
