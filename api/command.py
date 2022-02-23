import sys

from api.repositories.tweets import Tweets
from api.services.user_tweets import get_user_tweets
from api.services.user_lookup import lookup_user
from api.services.tag_tweet import tag_tweet
from api.services.generate_stats import generate_stats

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

def tag(id):
    tweet = Tweets.get(id)
    print(tweet)
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
    # print(user)

commands = {
    'timeline': get_timeline,
    'tag_all': tag_all,
    'tag': tag,
    'stats': stats,
    'user': get_user,
}

args = sys.argv
if len(args) > 1:
    run_command(commands, args)
else:
    print('bad number of params')
