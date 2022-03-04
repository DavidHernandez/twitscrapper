from .create_group_task import create_group_task
from .user_mentions import user_mentions

def extract_main_mentions(handle):
    users = user_mentions(handle)
