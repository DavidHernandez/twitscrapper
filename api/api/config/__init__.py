import mongoengine as db
from . import config
from twarc.client2 import Twarc2

db.connect(
        config.MONGO_DB,
        host=config.MONGO_HOST,
        port=config.MONGO_PORT,
        username=config.MONGO_USER,
        password=config.MONGO_PASSWORD
        )
