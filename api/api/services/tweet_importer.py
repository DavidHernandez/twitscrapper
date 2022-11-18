import json
from .operations.tweet import Tweet

class TweetImporter:

    @staticmethod
    def import_file(filename):
        file = open(f"./data/{filename}")
        data = json.load(file)

        for i in data:
            Tweet.tweet(i) 

        file.close()
