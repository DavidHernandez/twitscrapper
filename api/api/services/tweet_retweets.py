from api.repositories.tweets import Tweets

from ..models.user import User
from ..wrappers.twitter import twitter

def tweet_retweets(tweet_id):
    tweet = Tweets.get(tweet_id)

    if tweet.has('retweets'):
        return

    users = twitter.retweeted_by(tweet_id)

    new_users = []
    for data in users:
        for user_data in data['data']:
            user = User.from_json(user_data)
            tweet.add_retweeter(user.id)
            new_users.append(user)

    tweet.save()

    return new_users
