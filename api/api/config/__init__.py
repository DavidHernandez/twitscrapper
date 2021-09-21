import mongoengine as db
from . import config
from twarc import Twarc

db.connect(
        config.MONGO_DB,
        host=config.MONGO_HOST,
        port=config.MONGO_PORT,
        username=config.MONGO_USER,
        password=config.MONGO_PASSWORD
        )

twitter = Twarc(
        config.TWITTER_CONSUMER_KEY,
        config.TWITTER_CONSUMER_SECRET,
        config.TWITTER_TOKEN,
        config.TWITTER_TOKEN_SECRET
        )
