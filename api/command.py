import sys

from api.services.user_list import get_user_list
from api.services.operations.tag import Tag
from api.services.operations.user import User
from api.services.operations.tweet import Tweet
from api.services.projects.audience_project import AudienceProject


def run_command(arguments):
    if arguments[1] not in commands:
        print('invalid command')
        return

    if len(arguments) > 3:
        commands[arguments[1]](arguments[2], arguments[3])
    elif len(arguments) > 2:
        commands[arguments[1]](arguments[2])
    else:
        commands[arguments[1]]()

    print('Done')
    return

def get_list_memberships(handle):
    print('Getting list from @' + handle)
    list_memberships = get_user_list(handle)
    print('Imported ' + str(len(list_memberships)) + ' memberships from list')


commands = {
    'membership_list': get_list_memberships,
    'tag_all': Tag.all,
    'tag_tweets_of': Tag.by_handle,
    'tag': Tag.by_id,
    'user': User.get,
    'timeline': User.tweets,
    'mentions': User.mentions,
    'followers': User.followers,
    'tweet_retweets': Tweet.retweets,
    'all_retweets': Tweet.all_retweets,
    'tweet_likes': Tweet.likes,
    'all_likes': Tweet.all_likes,
    'tweet_replies': Tweet.replies,
    'all_replies': Tweet.all_replies,
    'create_project': AudienceProject.create,
}

args = sys.argv
if len(args) > 1:
    run_command(args)
else:
    print('bad number of params')
