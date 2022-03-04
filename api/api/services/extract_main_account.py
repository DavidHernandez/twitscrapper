from .user_lookup import lookup_user
from .create_group_task import create_group_task

def extract_main_account(handle):
    user = lookup_user(handle)

    create_group_task('extract_main_tweets', [handle])
    create_group_task('extract_main_mentions', [handle])
    create_group_task('extract_main_followers', [handle])
