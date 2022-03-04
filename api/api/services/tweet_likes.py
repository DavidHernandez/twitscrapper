from api.repositories.tweets import Tweets

from ..models.user import User
from ..wrappers.twitter import twitter

def tweet_likes(tweet_id):
    tweet = Tweets.get(tweet_id)

    if tweet.has('likes'):
        return

    users = twitter.liking_users(tweet_id)

    new_users = []
    for data in users:
        for user_data in data['data']:
            user = User.from_json(user_data)
            tweet.add_like(user.id)
            new_users.append(user)

    tweet.save()

    return new_users
