from api.models.stat import TopTagsStat

from api.repositories.tweets import Tweets
from api.repositories.stats import TopTagsStats

class TopTags:

    @staticmethod
    def calculate():
        TopTagsStats.clear()

        tweets = Tweets.with_tags()

        for tweet in tweets:
            tagged = tweet.tagged

            for tagged_kb in tagged:
                for tag in tagged_kb.tags:
                    tag_name = tag.tag
                    author = tweet.author_id
                    language = tweet.language
                    score = tweet.impact_score

                    all_stat = TopTagsStats.find(tag_name, 'all', author)
                    if not all_stat:
                        all_stat = TopTagsStat(
                            tag=tag_name,
                            user_id=author,
                            language='all',
                            times=0,
                            impact_score=2
                            )

                    all_stat.times += 1
                    all_stat.impact_score += score
                    all_stat.save()

                    lang_stat = TopTagsStats.find(tag_name, language, author)
                    if not lang_stat:
                        lang_stat = TopTagsStat(
                            tag=tag_name,
                            user_id=author,
                            language=language,
                            times=0,
                            impact_score=2
                            )

                    lang_stat.times += 1
                    lang_stat.impact_score += score
                    lang_stat.save()
