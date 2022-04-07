from ...repositories.tweets import Tweets
from ...repositories.users import Users
from ...wrappers.twitter import twitter
from ...models.user import User as Model
from ...models.tweet import Tweet


class User():
    @staticmethod
    def get(handle):
        if handle.isdigit():
            user_id = handle
            user = Users.by_id(user_id)
        else:
            user = Users.get(handle)
            if not user:
                user = User.profile(handle)
        return user

    @staticmethod
    def profile(handle):
        users = twitter.user_lookup([handle])
        for data in users:
            for user_data in data['data']:
                user = Model.from_json(user_data)
        return user

    @staticmethod
    def followers(handle):
        user = User.get(handle)
        user_id = user['id']

        if user.has('followers'):
            return []

        users = twitter.followers(user_id)
        user.mark('followers')
        for data in users:
            for user_data in data['data']:
                Model.from_json(user_data)

    @staticmethod
    def mentions(handle):
        user = User.get(handle)
        user_id = user['id']

        if user.has('mentions'):
            return []

        mentions = twitter.mentions(user_id)
        user.mark('mentions')
        user.save()

        for page in mentions:
            for mention_data in page['data']:
                tweet = Tweet.from_json(mention_data)

    @staticmethod
    def tweets(handle):
        user = User.get(handle)
        user_id = user['id']

        since_id = None
        if user.has('tweets'):
            last_tweet = Tweets.last(user_id)
            since_id = last_tweet.id

        tweets = twitter.timeline(user_id, since_id)
        result = []

        for page in tweets:
            for tweet_data in page['data']:
                Tweet.from_json(tweet_data)
