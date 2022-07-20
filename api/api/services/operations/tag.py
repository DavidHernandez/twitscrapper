from ...utils.tagger import Tagger
from ...repositories.tweets import Tweets
from ...repositories.users import Users

class Tag():

    @staticmethod
    def by_id(tweet_id):
        tweet = Tweets.get(id)
        Tag.tweet(tweet)

    @staticmethod
    def tweet(tweet):
        try:
            tagger_response = Tagger.tag(tweet.clean_text)
        except:
            # Error tagging, skipping
            print("Skipping because of error")
            return
        tags = tagger_response['result']['tags']
        tweet.untag()
        for tag in tags:
            tweet.add_tag(tag['knowledgebase'], True, tag['topic'], tag['subtopic'], tag['tag'], tag['times'])
        tweet.save()

    @staticmethod
    def tweets(tweets):
        for tweet in tweets:
            Tag.tweet(tweet)

    @staticmethod
    def all():
        tweets = Tweets.untagged()
        Tag.tweets(tweets)

    @staticmethod
    def by_handle(handle):
        user = Users.get(handle)
        tweets = Tweets.by_author(user.id)
        Tag.tweets(tweets)
