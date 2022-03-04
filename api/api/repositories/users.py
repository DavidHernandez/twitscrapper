from ..models.user import User 

class Users:

    @staticmethod
    def get(handle):
        return User.objects(handle=handle).first()

    @staticmethod
    def by_id(id):
        return User.objects(id=id).first()

    @staticmethod
    def all():
        return User.objects()
