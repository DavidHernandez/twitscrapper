from ..models.user import User 

class Users:

    @staticmethod
    def get(handle):
        return User.objects(handle=handle).first()

    @staticmethod
    def by_id(id):
        return User.objects(id=int(id)).first()

    @staticmethod
    def all():
        return User.objects()

    @staticmethod
    def by_query(query):
        return User.objects(__raw__=query)

    @staticmethod
    def untagged():
        return Users.by_query({'operations.profession': False}).batch_size(100)

    @staticmethod
    def top_followers(handle, limit=100):
        user = Users.get(handle)
        followers = user.follower_list
        return User.objects(id__in=followers).order_by('-followers').limit(limit)
