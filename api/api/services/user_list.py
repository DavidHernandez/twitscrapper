from ..wrappers.twitter import twitter
from ..repositories.users import Users
from ..models.list import List
from .user_lookup import lookup_user

def get_user_list(handle):
    if handle.isdigit():
        user_id = handle
        user = Users.by_id(user_id)
    else:
        user = Users.get(handle)
        if not user:
            user = lookup_user(handle)
        user_id = user['id']

    list_memberships = twitter.list_memberships(user_id)
    result = []

    
    for user_membership in list_memberships['data']:
        user_membership.update({'owner_list': str(user)}) 
        user = List.from_json(user_membership)
        result.append(user)
    return result
