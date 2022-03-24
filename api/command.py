import sys

from api.repositories.users import Users
from api.repositories.tweets import Tweets
from api.services.generate_stats import generate_stats
from api.services.tag_tweet import tag_tweet
from api.services.top_tweets import top_tweets
from api.services.tweet_likes import tweet_likes
from api.services.tweet_replies import tweet_replies
from api.services.tweet_retweets import tweet_retweets
from api.services.user_followers import user_followers
from api.services.user_lookup import lookup_user
from api.services.user_mentions import user_mentions
from api.services.user_tweets import get_user_tweets
from api.services.user_list import get_user_list

def run_command(commands, arguments):
    if arguments[1] not in commands:
        print('invalid command')
        return

    if len(arguments) > 2:
        return commands[arguments[1]](arguments[2])

    return commands[arguments[1]]()


def get_timeline(handle):
    print('Getting tweets from @' + handle)
    tweets = get_user_tweets(handle)
    print('Imported ' + str(len(tweets)) + ' tweets')

def get_list_memberships(handle):
    print('Getting list from @' + handle)
    listMemberships = get_user_list(handle)
    print('Imported ' + str(len(listMemberships)) + ' memberships from list')

def tag_all():
    tweets = Tweets.untagged()
    total = str(len(tweets))
    print('Tagging all ' + total + ' tweets')
    count = 1
    for tweet in tweets:
        print(str(count) + ' of ' + total)
        tag_tweet(tweet)
        count += 1
    print('Done')

def tag_tweets_of(handle):
    user = Users.get(handle)
    tweets = Tweets.by_author(user.id)
    total = str(len(tweets))
    print(f"Tagging {total} tweets of @{handle}")
    count = 1
    for tweet in tweets:
        print(str(count) + ' of ' + total)
        tag_tweet(tweet)
        count += 1
    print('Done')

def tag(id):
    tweet = Tweets.get(id)
    tag_tweet(tweet)

def stats():
    tweets = Tweets.all()
    total = str(len(tweets))
    print('Generating stats for ' + total + ' tweets')
    count = 1
    for tweet in tweets:
        print(str(count) + ' of ' + total)
        generate_stats(tweet)
        count += 1
    print('Done')

def get_user(handle):
    print('Getting profile from @' + handle)
    user = lookup_user(handle)
    print(user)

def mentions(handle):
    print('Getting mentions from @' + handle)
    mentions = user_mentions(handle)
    print('Done')

def followers(handle):
    print('Getting followers from @' + handle)
    followers = user_followers(handle)
    print('Done')

def single_tweet_retweets(tweet_id):
    print('Getting retweeters from tweet ' + tweet_id)
    tweet_retweets(tweet_id)
    print('Done')

def all_retweets():
    print('Getting retweeters from all tweets')
    tweets = Tweets.without_extracted_retweets()
    for tweet in tweets:
        print('Getting retweeters from tweet ' + tweet.id)
        tweet_retweets(tweet.id)
    print('Done')

def single_tweet_likes(tweet_id):
    print('Getting likes from tweet ' + tweet_id)
    tweet_likes(tweet_id)
    print('Done')

def all_likes():
    print('Getting likes from all tweets')
    tweets = Tweets.without_extracted_likes()
    for tweet in tweets:
        print('Getting likes from tweet ' + tweet.id)
        tweet_likes(tweet.id)
    print('Done')

def single_tweet_replies(tweet_id):
    print('Getting replies from tweet ' + tweet_id)
    tweet_replies(tweet_id)
    print('Done')

def all_replies():
    print('Getting replies from all tweets')
    tweets = Tweets.without_extracted_replies()
    for tweet in tweets:
        print('Getting replies from tweet ' + tweet.id)
        tweet_replies(tweet.id)
    print('Done')

def account_top_tweets(handle):
    print(f'Getting top tweets from {handle}')
    tweets = top_tweets(handle)
    print(tweets)

commands = {
    'timeline': get_timeline,
    'membership_list': get_list_memberships,
    'tag_all': tag_all,
    'tag_tweets_of': tag_tweets_of,
    'tag': tag,
    'stats': stats,
    'user': get_user,
    'mentions': mentions,
    'followers': followers,
    'tweet_retweets': single_tweet_retweets,
    'all_retweets': all_retweets,
    'tweet_likes': single_tweet_likes,
    'all_likes': all_likes,
    'tweet_replies': single_tweet_replies,
    'all_replies': all_replies,
    'top_tweets': account_top_tweets,
}

args = sys.argv
if len(args) > 1:
    run_command(commands, args)
else:
    print('bad number of params')
