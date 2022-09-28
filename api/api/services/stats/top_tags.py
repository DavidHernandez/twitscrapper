from api.models.stat import TopTagsStat

from api.repositories.tweets import Tweets
from api.repositories.stats import TopTagsStats

class TopTags:

    @staticmethod
    def calculate():
        TopTagsStats.clear()

        tweets = Tweets.with_tags()
        tags = {}
        tags['all'] = {}
        for tweet in tweets:
            language = tweet.language
            if language not in tags:
                tags[language] = {}

            tagged = tweet.tagged

            for tagged_kb in tagged:
                for tag in tagged_kb.tags:
                    tag_name = tag.tag

                    if tag_name not in tags['all']:
                        tags['all'][tag_name] = {
                                    'tag': tag_name,
                                    'times': 0,
                                    'user_id': tweet.author_id
                                }

                    if tag_name not in tags[language]:
                        tags[language][tag_name] = {
                                    'tag': tag_name,
                                    'times': 0,
                                    'user_id': tweet.author_id
                                }
                    tags['all'][tag_name]['times'] += 1
                    tags[language][tag_name]['times'] += 1


        for language in tags:
            for tag_name in tags[language]:
                tag = tags[language][tag_name] 
                TopTagsStat(
                    tag=tag['tag'],
                    times=tag['times'],
                    user_id=tag['user_id'],
                    language=language
                    ).save()
