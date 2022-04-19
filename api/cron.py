from api.repositories.projects import Projects
from api.repositories.operations import Operations
from api.services.operations.tag import Tag
from api.services.operations.user import User
from api.services.operations.tweet import Tweet
from api.services.projects.audience_project import AudienceProject

def do_nothing(*args):
    # command not implemented
    pass

commands = {
    'extract_account': User.get,
    'extract_tweets': User.tweets,
    'tag_tweets': Tag.by_handle,
    'extract_likes': Tweet.likes,
    'extract_retweets': Tweet.retweets,
    'extract_mentions': User.mentions,
    'extract_replies': Tweet.replies,
    'extract_followers': User.followers,
    'tag_users': do_nothing,
    'extract_lists': do_nothing,
    'extract_list_members': do_nothing,
}

limits = {
    'extract_account': 10,
    'extract_tweets': 1,
    'tag_tweets': None,
    'extract_likes': 1,
    'extract_retweets': 1,
    'extract_mentions': 450,
    'extract_replies': 450,
    'extract_followers': 1,
    'tag_users': None,
    'extract_lists': 75,
    'extract_list_members': 900,
}

def run_command(command_name, arguments):
    command = commands[command_name]
    if len(arguments) > 1:
        command(arguments[0], arguments[1])
    else:
        command(arguments[0])


def execute_operations():
    print('Executing operations')
    executed_operations = []
    for command_name in commands:
        limit = commands[command_name]

        operations = Operations.by_command_type(command_name, limit)
        for operation in operations:
            parameters = operation.parameters
            run_command(command_name, parameters)
            operation.complete()
            executed_operations.append(operation.id)

    return executed_operations
    print('Operations done')

def review_projects(operations):
    projects = Projects.active()
    for project in projects:
        audience_project = AudienceProject(project)
        audience_project.update_status(operations)

def cron():
    print('Starting cron')
    operations = execute_operations()
    review_projects(operations)
    print('Cron ended')

cron()
