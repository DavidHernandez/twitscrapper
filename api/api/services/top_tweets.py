from ..repositories.users import Users
from ..repositories.tweets import Tweets
from .user_lookup import lookup_user

def top_tweets(handle):
    if handle.isdigit():
        user_id = handle
        user = Users.by_id(user_id)
    else:
        user = Users.get(handle)
        if not user:
            users = lookup_user(handle)
            user = users[0] 
        user_id = user['id']

    print(user_id)
    tweets = Tweets.top_by_account(user_id)

    return tweets
