from .tag_tweet import tag_tweet

def tag_tweets(tweets):
    for tweet in tweets:
        tag_tweet(tweet)
