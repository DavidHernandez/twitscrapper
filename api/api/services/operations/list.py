from ...wrappers.twitter import twitter
from ...models.list import List as Model
from .user import User

class List():

    @staticmethod
    def user_is_member(handle):
        user = User.get(handle)
        user_id = user['id']

        list_memberships = twitter.list_memberships(user_id)
        result = []
    
        for data in list_memberships:
            for list_data in data['data']:
                twitter_list = Model.from_json(list_data)
                twitter_list.add_member(user_id)
                result.append(twitter_list)
        return result
