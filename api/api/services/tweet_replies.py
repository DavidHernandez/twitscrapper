from api.repositories.tweets import Tweets

from ..models.tweet import Tweet
from ..wrappers.twitter import twitter

def tweet_replies(tweet_id):
    tweet = Tweets.get(tweet_id)

    if tweet.has('replies'):
        return

    conversation_id = tweet.raw['conversation_id']
    tweets = twitter.replies(conversation_id)

    new_tweets = []
    for data in tweets:
        for tweet_data in data['data']:
            new_tweet = Tweet.from_json(tweet_data)
            tweet.add_reply(new_tweet.id)
            new_tweets.append(new_tweet)

    tweet.save()

    return new_tweets
