from api.models.stat import TopTopicsStat

from api.repositories.tweets import Tweets
from api.repositories.stats import TopTopicsStats

class TopTopics:

    @staticmethod
    def calculate():
        TopTopicsStats.clear()

        tweets = Tweets.all()
        topics = {}
        topics['all'] = {}
        for tweet in tweets:
            if not tweet.has_tags():
                continue

            language = tweet.language
            if language not in topics:
                topics[language] = {}

            tagged = tweet.tagged

            for tagged_kb in tagged:
                for tag in tagged_kb.tags:
                    topic = tag.subtopic

                    if topic not in topics['all']:
                        topics['all'][topic] = {
                                    'topic': topic,
                                    'times': 0,
                                    'user_id': tweet.author_id
                                }

                    if topic not in topics[language]:
                        topics[language][topic] = {
                                    'topic': topic,
                                    'times': 0,
                                    'user_id': tweet.author_id
                                }
                    topics['all'][topic]['times'] += 1
                    topics[language][topic]['times'] += 1


        for language in topics:
            for topic_name in topics[language]:
                topic = topics[language][topic_name] 
                TopTopicsStat(
                    topic=topic['topic'],
                    times=topic['times'],
                    user_id=topic['user_id'],
                    language=language
                    ).save()
