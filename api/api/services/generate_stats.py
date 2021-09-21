from ..repositories.stats import Stats
from datetime import datetime


def generate_stats(tweet):
    format = '%a %b %d %H:%M:%S %z %Y'
    date = datetime.strptime(tweet.created, format)
    day = date.strftime('%d')
    month = date.strftime('%m')
    year = date.strftime('%Y')

    day_stats = Stats.get_or_create(year, month, day, 'daily', tweet.author.handle)
    month_stats = Stats.get_or_create(year, month, '00', 'monthly', tweet.author.handle)
    year_stats = Stats.get_or_create(year, '00', '00', 'yearly', tweet.author.handle)
    all_time_stats = Stats.get_or_create('00', '00', '00', 'alltime', tweet.author.handle)

    _add_stats_from_tweet(day_stats, tweet)
    _add_stats_from_tweet(month_stats, tweet)
    _add_stats_from_tweet(year_stats, tweet)
    _add_stats_from_tweet(all_time_stats, tweet)

def _add_stats_from_tweet(stat, tweet):
    stat.add_likes(tweet.liked)
    stat.add_retweets(tweet.retweeted)
    stat.increment_tweets()
    stat.add_lang(tweet.language)

    for kb in tweet.tagged:
        for tag in kb.tags:
            stat.add_tag(tag)

    for hashtag in tweet.entities.urls:
        tweet.add_hashtag(hashtag.url)

    for mention in tweet.entities.mentions:
        tweet.add_mention(mention.handle)

    stat.save()
