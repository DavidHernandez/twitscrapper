from ..models.user import User
from ..repositories.users import Users
from ..wrappers.twitter import twitter
from .user_lookup import lookup_user

def user_followers(handle):
    if handle.isdigit():
        user_id = handle
        user = Users.by_id(user_id)
    else:
        user = Users.get(handle)
        if not user:
            users = lookup_user(handle)
            user = users[0] 
        user_id = user['id']

    if user.has('followers'):
        return []

    users = twitter.followers(user_id)
    user.mark('followers')
    new_users = []
    for data in users:
        for user_data in data['data']:
            user = User.from_json(user_data)
            new_users.append(user)

    return new_users
