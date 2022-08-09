from api.repositories.users import Users
from api.repositories.stats import TopFollowersStats, TopHashtagsStats
from api.repositories.tweets import Tweets
from api.models.stat import TopHashtagsStat


class TopHashtags:

    @staticmethod
    def calculate(handle, skip=False):
        if not skip:
            TopHashtagsStats.clear()

        main = Users.get(handle)

        tweets = Tweets.by_author(main.id)
        hashtags = {}
        hashtags['all'] = {}

        for tweet in tweets:
            language = tweet.language
            if language not in hashtags:
                hashtags[language] = {}

            if tweet.hashtags:
                for hashtag in tweet.hashtags:
                    if hashtag not in hashtags['all']:
                        hashtags['all'][hashtag] = 0

                    if hashtag not in hashtags[language]:
                        hashtags[language][hashtag] = 0

                    hashtags['all'][hashtag] += 1
                    hashtags[language][hashtag] += 1

        for language in hashtags:
            for hashtag in hashtags[language]:
                times = hashtags[language][hashtag]
                TopHashtagsStat(
                        user_id=main.id,
                        user_handle=main.handle,
                        hashtag=hashtag,
                        times=times,
                        language=language
                        ).save()

        if not skip:
            followers = TopFollowersStats.by_user(handle)
            for follower in followers:
                TopHashtags.calculate(follower.follower_handle, skip=True)
