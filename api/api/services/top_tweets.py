from ..repositories.users import Users
from ..repositories.tweets import Tweets
from .operations.user import User

def top_tweets(handle):
    user = User.get(handle)
    user_id = user['id']

    print(user_id)
    tweets = Tweets.top_by_account(user_id)

    return tweets
