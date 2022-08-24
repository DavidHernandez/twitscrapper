from ..models.stat import TopFollowersStat, TopHashtagsStat, TopMentionsStat

class TopFollowersStats:

    @staticmethod
    def by_user(handle):
        return TopFollowersStat.objects(user_handle=handle)

    @staticmethod
    def follower_of_follower_by_user(handle):
        return TopFollowersStat.objects(user_handle__ne=handle, ranking__lte=10)

    @staticmethod
    def clear():
        return TopFollowersStat.objects().delete()

class TopMentionsStats:

    @staticmethod
    def clear():
        return TopMentionsStat.objects().delete()

class TopHashtagsStats:

    @staticmethod
    def clear():
        return TopHashtagsStat.objects().delete()
