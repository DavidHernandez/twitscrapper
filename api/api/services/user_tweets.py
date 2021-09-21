from ..config import twitter
from ..models.tweet import Tweet

def get_user_tweets(handle):
    tweets = twitter.timeline(screen_name=handle)
    result = []
    for tweet_data in tweets:
        tweet = Tweet(
            id=tweet_data['id'],
            created=tweet_data['created_at'],
            text=tweet_data['full_text'],
            retweeted=tweet_data['retweet_count'],
            liked=tweet_data['favorite_count'],
            language=tweet_data['lang']
        )

        tweet.add_author()
        tweet.author.id = tweet_data['user']['id']
        tweet.author.name = tweet_data['user']['name']
        tweet.author.handle = tweet_data['user']['screen_name']
        tweet.author.followers = tweet_data['user']['followers_count']
        tweet.author.following = tweet_data['user']['friends_count']
        tweet.author.tweets = tweet_data['user']['statuses_count']
        tweet.author.profile_pic = tweet_data['user']['profile_image_url_https']

        for hashtag in tweet_data['entities']['hashtags']:
            tweet.add_hashtag(hashtag['text'])

        for url in tweet_data['entities']['urls']:
            tweet.add_url(url['url'], url['expanded_url'])

        for mention in tweet_data['entities']['user_mentions']:
            tweet.add_mention(mention['id'], mention['name'], mention['screen_name'])

        tweet.save()

        result.append(tweet)
    return result
