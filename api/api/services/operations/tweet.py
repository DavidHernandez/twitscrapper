from ...repositories.tweets import Tweets
from ...repositories.users import Users
from ...wrappers.twitter import twitter
from ...models.user import User
from ...models.tweet import Tweet as Model

class Tweet():

    @staticmethod
    def likes(tweet_id):
        tweet = Tweets.get(tweet_id)

        if tweet.has('likes'):
            return

        users = twitter.liking_users(tweet_id)

        for data in users:
            for user_data in data['data']:
                user_id = user_data['id']
                if not Users.exists(user_id):
                    user = User.from_json(user_data)
                tweet.add_like(user_id)

        tweet.save()

    @staticmethod
    def all_likes():
        tweets = Tweets.without_extracted_likes()

        for tweet in tweets:
            Tweet.likes(tweet.id)

    @staticmethod
    def retweets(tweet_id):
        tweet = Tweets.get(tweet_id)

        if tweet.has('retweets'):
            return

        users = twitter.retweeted_by(tweet_id)

        for data in users:
            for user_data in data['data']:
                user_id = user_data['id']
                if not Users.exists(user_id):
                    user = User.from_json(user_data)
                tweet.add_retweeter(user_id)

        tweet.save()

    @staticmethod
    def all_retweets():
        tweets = Tweets.without_extracted_retweets()
        for tweet in tweets:
            Tweet.retweets(tweet.id)

    @staticmethod
    def replies(tweet_id):
        tweet = Tweets.get(tweet_id)

        if tweet.has('replies'):
            return

        conversation_id = tweet.raw['conversation_id']
        tweets = twitter.replies(conversation_id)

        for data in tweets:
            for tweet_data in data['data']:
                tweet_id = tweet_data['id']
                if not Tweets.get(tweet_id):
                    new_tweet = Model.from_json(tweet_data)
                tweet.add_reply(tweet_id)

        tweet.save()

    @staticmethod
    def all_replies():
        tweets = Tweets.without_extracted_replies()

        for tweet in tweets:
            Tweet.replies(tweet.id)
