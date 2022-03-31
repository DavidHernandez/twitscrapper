from os import environ as env


MONGO_HOST = env.get('MONGO_HOST', 'localhost')
MONGO_DB = env.get('MONGO_DB_NAME', 'twitscrapper')
MONGO_PORT = int(env.get('MONGO_PORT', '27017'))
MONGO_USER = env.get('MONGO_USER', 'twitscrapper')
MONGO_PASSWORD = env.get('MONGO_PASSWORD', 'twitscrapper')

NEO_URI = env.get('MONGO_HOST', 'bolt://localhost:7687')

TWITTER_CONSUMER_KEY = env.get('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = env.get('TWITTER_CONSUMER_SECRET', '')
TWITTER_TOKEN = env.get('TWITTER_TOKEN', '')
TWITTER_TOKEN_SECRET = env.get('TWITTER_TOKEN_SECRET', '')

BACKEND_URL = env.get('BACKEND_URL', 'http://localhost:5000')
