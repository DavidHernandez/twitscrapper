from ..utils.tagger import tag_text

def tag_tweet(tweet):
    tagger_response = tag_text(tweet.text)
    tags = tagger_response['result']['tags']
    tweet.untag()
    for tag in tags:
        tweet.add_tag(tag['knowledgebase'], True, tag['topic'], tag['subtopic'], tag['tag'], tag['times'])
    tweet.save()
