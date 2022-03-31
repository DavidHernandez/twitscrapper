from ..config import config
import requests

def tag_text(text):
    r = requests.post(config.BACKEND_URL + '/tagger/',
        data={'text': text}
    )

    return r.json()
