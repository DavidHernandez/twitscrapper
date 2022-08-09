from api.repositories.users import Users
from api.repositories.stats import TopFollowersStats
from api.models.stat import TopFollowersStat


class TopFollowers:
    @staticmethod
    def calculate(handle, skip=False):
        if not skip:
            TopFollowersStats.clear()

        main = Users.get(handle)
        users = Users.top_followers(handle)
        count = 1
        for user in users:
            TopFollowersStat(
                    user_id=main.id,
                    user_handle=main.handle,
                    follower_id=user.id,
                    follower_handle=user.handle,
                    ranking=count,
                    followers=user.followers,
                    verified=user.verified,
                    profession=user.profession
                    ).save()
            count += 1
            if not skip:
                TopFollowers.calculate(user.handle, skip=True)
