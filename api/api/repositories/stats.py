from ..models.stat import TopFollowersStat

class TopFollowersStats:

    @staticmethod
    def clear():
        return TopFollowersStat.objects().delete()
