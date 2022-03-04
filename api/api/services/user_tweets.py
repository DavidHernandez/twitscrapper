from ..wrappers.twitter import twitter
from ..models.tweet import Tweet
from ..repositories.users import Users
from .user_lookup import lookup_user

def get_user_tweets(handle):
    if handle.isdigit():
        user_id = handle
        user = Users.by_id(user_id)
    else:
        user = Users.get(handle)
        if not user:
            user = lookup_user(handle)
        user_id = user['id']

    tweets = twitter.timeline(user_id)
    result = []

    for page in tweets:
        for tweet_data in page['data']:
            tweet = Tweet.from_json(tweet_data)
            result.append(tweet)

    return result
