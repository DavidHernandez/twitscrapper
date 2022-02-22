from ..models.user import User 

class Users:

    @staticmethod
    def get(handle):
        return User.objects(handle=handle).first()
