from ..wrappers.twitter import twitter
from ..models.user import User

def lookup_user(handle):
    users = twitter.user_lookup([handle])
    for data in users:
        for user_data in data['data']:
            user = User.from_json(user_data)

            return user
