from ..config import twitter
from ..models.user import User

def lookup_user(user_name):
    users = twitter.user_lookup([user_name], usernames=True)
    new_users = []
    for data in users:
        for user_data in data['data']:
            metrics = user_data['public_metrics']
            user = User(
                id=user_data['id'],
                handle=user_data['username'],
                name=user_data['name'],
                followers=metrics['followers_count'],
                following=metrics['following_count'],
                tweets=metrics['tweet_count'],
                profile_pic=user_data['profile_image_url'],
                description=user_data['description'],
                location=user_data['location'],
                url=user_data['url'],
                created_at=user_data['created_at'],
                verified=user_data['verified'],
            )
            user.save()
            new_users.append(user)

    return new_users
