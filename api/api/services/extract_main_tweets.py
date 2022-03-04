from .create_group_task import create_group_task
from .user_tweets import get_user_tweets

def extract_main_tweets(handle):
    tweets = get_user_tweets(handle)

    create_group_task('tag_main_tweets', tweets)
