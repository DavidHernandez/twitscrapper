from ..config import twitter
from ..models.tweet import Tweet
from ..repositories.users import Users
from .user_lookup import lookup_user

def get_user_tweets(handle):
    if handle.isdigit():
        user_id = handle
    else:
        try:
            user = Users.get(handle)
        except:
            users = lookup_user(handle)
            user = users[0] 
        user_id = user['id']

    tweets = twitter.timeline(user_id)
    result = []

    for page in tweets:
        for tweet_data in page['data']:
            metrics = tweet_data['public_metrics']

            tweet = Tweet(
                id=tweet_data['id'],
                author_id=tweet_data['author_id'],
                created=tweet_data['created_at'],
                text=tweet_data['text'],

                retweeted=metrics['retweet_count'],
                liked=metrics['like_count'],
                replies=metrics['reply_count'],
                quotes=metrics['quote_count'],

                language=tweet_data['lang'],

                raw=tweet_data
            )

            if 'entities' in tweet_data:
                entities = tweet_data['entities']
                if 'hashtags' in entities:
                    for hashtag in entities['hashtags']:
                        tweet.add_hashtag(hashtag['tag'])

                if 'urls' in entities:
                    for url in entities['urls']:
                        tweet.add_url(url['expanded_url'])

                if 'user_mentions' in entities:
                    for mention in entities['user_mentions']:
                        tweet.add_mention(mention['id'], mention['username'])

            tweet.calculate_impact_score()
            tweet.save()
            result.append(tweet)

    return result

