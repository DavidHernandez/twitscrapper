from ..wrappers.twitter import twitter
from ..repositories.users import Users
from .user_lookup import lookup_user
from ..models.tweet import Tweet

def user_mentions(handle):
    if handle.isdigit():
        user_id = handle
        user = Users.by_id(user_id)
    else:
        user = Users.get(handle)
        if not user:
            users = lookup_user(handle)
            user = users[0] 
        user_id = user['id']

    if user.has('mentions'):
        return []

    mentions = twitter.mentions(user_id)
    user.mark('mentions')
    user.save()
    result = []

    for page in mentions:
        for mention_data in page['data']:
            tweet = Tweet.from_json(mention_data)
            result.append(tweet)

    return result
