import sys

from api.services.operations.list import List
from api.services.operations.tag import Tag
from api.services.operations.tweet import Tweet
from api.services.operations.user import User
from api.services.projects.audience_project import AudienceProject
from api.services.stats.top_followers import TopFollowers
from api.services.tag_updater import TagUpdater


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


commands = {
    'membership_list': List.user_is_member,
    'tag_all': Tag.all,
    'tag_profiles': Tag.profiles,
    'tag_tweets_of': Tag.by_handle,
    'tag': Tag.by_id,
    'update-kb': TagUpdater.execute,
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
    'top_followers': TopFollowers.calculate,
}

args = sys.argv
if len(args) > 1:
    run_command(args)
else:
    print('bad number of params')
