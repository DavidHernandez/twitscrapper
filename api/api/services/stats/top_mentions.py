from api.repositories.users import Users
from api.repositories.stats import TopFollowersStats, TopMentionsStats
from api.repositories.tweets import Tweets
from api.models.stat import TopMentionsStat


class TopMentions:

    @staticmethod
    def calculate(handle, skip=False):
        if not skip:
            TopMentionsStats.clear()

        main = Users.get(handle)

        tweets = Tweets.by_author(main.id)
        mentions = {}
        mentions['all'] = {}

        for tweet in tweets:
            language = tweet.language
            if language not in mentions:
                mentions[language] = {}

            if tweet.mentions:
                for mention in tweet.mentions:
                    if mention.id not in mentions['all']:
                        mentions['all'][mention.id] = {
                                    'id': mention.id,
                                    'handle': mention.handle,
                                    'times': 0
                                }

                    if mention.id not in mentions[language]:
                        mentions[language][mention.id] = {
                                    'id': mention.id,
                                    'handle': mention.handle,
                                    'times': 0
                                }

                    mentions['all'][mention.id]['times'] += 1
                    mentions[language][mention.id]['times'] += 1

        for language in mentions:
            for mention_id in mentions[language]:
                mention = mentions[language][mention_id]
                TopMentionsStat(
                        user_id=main.id,
                        user_handle=main.handle,
                        mentioned_id=mention['id'],
                        mentioned_handle=mention['handle'],
                        times=mention['times'],
                        language=language
                        ).save()

        if not skip:
            followers = TopFollowersStats.by_user(handle)
            for follower in followers:
                TopMentions.calculate(follower.follower_handle, skip=True)
