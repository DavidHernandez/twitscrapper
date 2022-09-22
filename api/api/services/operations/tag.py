from ...utils.tagger import Tagger
from ...repositories.tweets import Tweets
from ...repositories.users import Users

class Tag():

    @staticmethod
    def by_id(tweet_id):
        tweet = Tweets.get(tweet_id)
        Tag.tweet(tweet)

    @staticmethod
    def tweet(tweet):
        kb = 'isglobal-ods3-' + tweet.language
        try:
            tagger_response = Tagger.tag(kb, tweet.text)
        except Exception as e:
            # Error tagging, skipping
            print("Skipping because of error")
            print(e)
            return
        tags = tagger_response['result']['tags']
        tweet.untag()
        for tag in tags:
            tweet.add_tag(tag['knowledgebase'], True, tag['topic'], tag['subtopic'], tag['tag'], tag['times'])
        tweet.save()

    @staticmethod
    def profile(user):
        print(f"Tagging {user}")
        kb = 'profesiones'
        try:
            tagger_response = Tagger.tag(kb, user.description)
        except Exception as e:
            # Error tagging, skipping
            print("Skipping because of error")
            print(e)
            return
        tags = tagger_response['result']['tags']
        user.untag()
        for tag in tags:
            user.add_tag(tag['knowledgebase'], True, tag['topic'], tag['subtopic'], tag['tag'], tag['times'])
        user.save()

    @staticmethod
    def tweets(tweets):
        for tweet in tweets:
            Tag.tweet(tweet)

    @staticmethod
    def all():
        tweets = Tweets.untagged()
        Tag.tweets(tweets)

    @staticmethod
    def untag_all():
        tweets = Tweets.tagged()
        for tweet in tweets:
            tweet.untag()
            tweet.save()

    @staticmethod
    def retag_all():
        tweets = Tweets.all()
        Tag.tweets(tweets)

    @staticmethod
    def profiles():
        users = Users.untagged()
        for user in users:
            Tag.profile(user)

    @staticmethod
    def by_handle(handle):
        user = Users.get(handle)
        tweets = Tweets.by_author(user.id)
        Tag.tweets(tweets)
