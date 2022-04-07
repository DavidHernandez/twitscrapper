from datetime import datetime
from .base_project import BaseProject
from ...models.operation import Operation
from ...models.project import Project
from ...repositories.operations import Operations
from ...repositories.projects import Projects
from ...repositories.tweets import Tweets
from ...repositories.users import Users

class AudienceProject(BaseProject):

    @staticmethod
    def create(account, knowledge_base):
        data = {
                    'account': account,
                    'knowledge_base': knowledge_base,
                }
        project = Project(type='audience', data=data)
        project.save()

        audience_project = AudienceProject(project)
        audience_project.add_tasks()

        return audience_project

    @staticmethod
    def from_id(project_id):
        project = Projects.get(project_id)

        return AudienceProject(project)

    def get_handle(self):
        return self.project.data['account']

    def get_kb(self):
        return self.project.data['knowledge_base']

    def main_account_profile_parameters(self):
        return [self.get_handle()]

    def main_account_tweets_parameters(self):
        return [self.get_handle()]

    def main_account_mentions_parameters(self):
        return [self.get_handle()]

    def main_account_lists_parameters(self):
        return [self.get_handle()]

    def main_account_followers_parameters(self):
        return [self.get_handle()]

    def main_account_tagged_tweets_parameters(self):
        return [self.get_handle(), self.get_kb()]

    def main_account_tweets_likes_parameters(self):
        handle = self.get_handle()
        user = Users.get(handle)

        tweets = Tweets.top_liked_from_account(user.id).limit(100)
        ids = []
        for tweet in tweets:
            ids.append(str(tweet.id))

        return ids 

    def main_account_tweets_retweets_parameters(self):
        handle = self.get_handle()
        user = Users.get(handle)

        tweets = Tweets.top_retweeted_from_account(user.id).limit(100)
        ids = []
        for tweet in tweets:
            ids.append(str(tweet.id))

        return ids 

    def main_account_tweets_replies_parameters(self):
        handle = self.get_handle()
        user = Users.get(handle)

        tweets = Tweets.top_replied_from_account(user.id).limit(100)
        ids = []
        for tweet in tweets:
            ids.append(str(tweet.id))

        return ids 

    def follower_users_tweets_parameters(self):
        handle = self.get_handle()
        top_followers = Users.top_followers(handle)

        handles = []
        for user in top_followers:
            handles.append(str(user.handle))
        return handles

    def followers_followers_parameters(self):
        return self.follower_users_tweets_parameters()

    def followers_followers_tweets_parameters(self):
        handle = self.get_handle()
        top_followers = Users.top_followers(handle)

        handles = []
        for user in top_followers:
            top_follower_followers = Users.top_followers(user.handle, 10)
            for user_follower in top_followers:
                handles.append(str(user_follower.handle))
        return handles

    def main_account_profile_operation(self, command, parameters):
        return self.create_standard_operation(command, parameters)

    def main_account_lists_operation(self, command, parameters):
        return self.create_standard_operation(command, parameters)

    def main_account_mentions_operation(self, command, parameters):
        return self.create_standard_operation(command, parameters)

    def main_account_followers_operation(self, command, parameters):
        return self.create_standard_operation(command, parameters)

    def main_account_tagged_tweets_operation(self, command, parameters):
        return self.create_standard_operation(command, parameters)

    def main_account_tweets_operation(self, command, parameters):
        hash_id = Operation.hash_id(command, parameters)
        operation = Operations.get(hash_id)

        if not operation:
            Operation(command=command, parameters=parameters).save()
            return [hash_id]

        date = datetime.now()
        current_date = str(date.year) + str(date.month).zfill(2)

        if int(operation.execution_date) < int(current_date):
            operation.execution_date = None
            operation.save()

        return [hash_id]

    def main_account_tweets_likes_operation(self, command, parameters):
        return self.create_standard_multioperation(command, parameters)

    def main_account_tweets_retweets_operation(self, command, parameters):
        return self.create_standard_multioperation(command, parameters)

    def main_account_tweets_replies_operation(self, command, parameters):
        return self.create_standard_multioperation(command, parameters)

    def follower_users_tweets_operation(self, command, parameters):
        return self.create_standard_multioperation(command, parameters)

    def followers_followers_operation(self, command, parameters):
        return self.create_standard_multioperation(command, parameters)

    def followers_followers_tweets_operation(self, command, parameters):
        return self.follower_users_tweets_operation(command, parameters)

    def get_project_tasks(self):
        return [{
            'name': 'main_account_profile',
            'command': 'extract_account',
            'child_tasks': [{
                'name': 'main_account_tweets',
                'command': 'extract_tweets',
                'child_tasks': [{
                    # 'name': 'main_account_tagged_tweets',
                    # 'command': 'tag_tweets',
                # },
                # {
                    'name': 'main_account_tweets_likes',
                    'command': 'extract_likes',
                },
                {
                    'name': 'main_account_tweets_retweets',
                    'command': 'extract_retweets',
                },
                {
                    'name': 'main_account_tweets_replies',
                    'command': 'extract_replies',
                }]
            },
            {
                'name': 'main_account_mentions',
                'command': 'extract_mentions',
                # 'child_tasks': [{
                    # 'name': 'tag_mention_users',
                    # 'command': 'tag_users',
                # }]
            },
            # {
                # 'name': 'main_account_lists',
                # 'command': 'extract_lists',
                # 'child_tasks': [{
                    # 'name': 'main_account_list_members',
                    # 'command': 'extract_list_members',
                    # 'child_tasks': [{
                        # 'name': 'tag_list_users',
                        # 'command': 'tag_users',
                    # }]
                # }]
            # },
            # {
                # 'name': 'main_account_quotes',
                # 'command': 'extract_quotes',
            # },
            {
                'name': 'main_account_followers',
                'command': 'extract_followers',
                'child_tasks': [{
                    'name': 'follower_users_tweets',
                    'command': 'extract_tweets',
                    # 'child_tasks': [{
                        # 'name': 'tag_follower_tweets',
                        # 'command': 'tag_tweets',
                    # }]
                },
                {
                    'name': 'followers_followers',
                    'command': 'extract_followers',
                    'child_tasks': [{
                        'name': 'followers_followers_tweets',
                        'command': 'extract_tweets',
                        # 'child_tasks': [{
                            # 'name': 'tag_followers_followers_tweets',
                            # 'command': 'tag_tweets',
                        # }],
                    # },
                    # {
                        # 'name': 'tag_followers_followers',
                        # 'command': 'tag_users',
                    }]
                # },
                # {
                    # 'name': 'tag_follower_users',
                    # 'command': 'tag_users',
                }],
            }],
        }]
