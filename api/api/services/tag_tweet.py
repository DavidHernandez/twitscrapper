from ..utils.tagger import tag_text

def tag_tweet(tweet):
    try:
        tagger_response = tag_text(tweet.clean_text)
    except:
        # Error tagging, skipping
        print("Skipping because of error")
        return
    tags = tagger_response['result']['tags']
    tweet.untag()
    for tag in tags:
        tweet.add_tag(tag['knowledgebase'], True, tag['topic'], tag['subtopic'], tag['tag'], tag['times'])
    tweet.save()
