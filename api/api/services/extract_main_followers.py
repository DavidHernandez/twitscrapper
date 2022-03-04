from .create_group_task import create_group_task
from .user_followers import user_followers

def extract_main_followers(handle):
    users = user_followers(handle)
