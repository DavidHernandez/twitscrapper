import sys

from api.services.operations.list import List
from api.services.operations.tag import Tag
from api.services.operations.tweet import Tweet
from api.services.operations.user import User
from api.services.projects.audience_project import AudienceProject
from api.services.stats.top_followers import TopFollowers
from api.services.stats.top_hashtags import TopHashtags
from api.services.stats.top_mentions import TopMentions
from api.services.stats.top_tags import TopTags
from api.services.stats.top_topics import TopTopics
from api.services.tag_updater import TagUpdater
from api.services.tweet_importer import TweetImporter


def run_command(arguments):
    if arguments[1] not in commands:
        print('invalid command')
        return

    if len(arguments) > 4:
        commands[arguments[1]](arguments[2], arguments[3], arguments[4])
    elif len(arguments) > 3:
        commands[arguments[1]](arguments[2], arguments[3])
    elif len(arguments) > 2:
        commands[arguments[1]](arguments[2])
    else:
        commands[arguments[1]]()

    print('Done')
    return


commands = {
    'tweet': Tweet.tweet,
    'membership_list': List.user_is_member,
    'tag_all': Tag.all,
    'untag_all': Tag.untag_all,
    'retag_all': Tag.retag_all,
    'tag_profiles': Tag.profiles,
    'tag_tweets_of': Tag.by_handle,
    'tag': Tag.by_id,
    'update-kb': TagUpdater.execute,
    'add-kb': TagUpdater.by_file,
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
    'top_mentions': TopMentions.calculate,
    'top_hashtags': TopHashtags.calculate,
    'top_topics': TopTopics.calculate,
    'top_tags': TopTags.calculate,
    'add_extra': User.add_extra,
    'user_delete': User.delete,
    'import': TweetImporter.import_file,
}

args = sys.argv
if len(args) > 1:
    run_command(args)
else:
    print('bad number of params')
