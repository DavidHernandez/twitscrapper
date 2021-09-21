from ..config import config
import requests
import json

def tag_text(text):
    r = requests.post(config.BACKEND_URL + '/tagger/',
        data={'text': text}
    )

    return r.json()
