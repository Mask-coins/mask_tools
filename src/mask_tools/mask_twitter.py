import datetime
import pandas as pd
import numpy as np
import pprint


def extract_tweets(tweet_full):
    if len(tweet_full)==1 and 'delete' in tweet_full:
        return None
    if 'retweeted_status' in tweet_full and tweet_full['retweeted_status'] is not None:
        return extract_tweets(tweet_full['retweeted_status'])
    if 'id' not in tweet_full:
        return {}
    tweet = dict()
    tweet['id'] = tweet_full['id']
    tweet['created_at'] = datetime.datetime.strptime(tweet_full['created_at'], '%a %b %d %H:%M:%S %z %Y')
    tweet['text'] = tweet_full['text']
    tweet['user_id'] = tweet_full['user']['id']
    tweet['user_name'] = tweet_full['user']['name']
    tweet['user_screen_name'] = tweet_full['user']['screen_name']
    tweet['location'] = tweet_full['user']['location']
    tweet['description'] = tweet_full['user']['description']
    tweet['entities_mentions'] = ''
    if 'entities' in tweet_full and not tweet_full['entities'] is None:
        if 'user_mentions' in tweet_full['entities'] and not tweet_full['entities']['user_mentions'] is None:
            for mentiond_user in tweet_full['entities']['user_mentions']:
                if mentiond_user['id_str'] is not None:
                    tweet['entities_mentions'] += mentiond_user['id_str'] + ','
                #print('Mention : ' + str(tweet['entities_mentions']))
    # このツイートがリプライの場合、オリジナルのツイートのuser_id
    tweet['in_reply_to_user_id'] = -1
    if 'in_reply_to_user_id' in tweet_full and not tweet_full['in_reply_to_user_id'] is None:
        tweet['in_reply_to_user_id'] = tweet_full['in_reply_to_user_id']
        #print('Reply : ' + str(tweet['in_reply_to_user_id']))

    if 'coordinates' in tweet_full and not tweet_full['coordinates'] is None:
        tweet['coordinate_lat'] = tweet_full['coordinates']['coordinates'][0]
        tweet['coordinate_long'] = tweet_full['coordinates']['coordinates'][1]
    else:
        tweet['coordinate_lat'] = -1
        tweet['coordinate_long'] = -1
    if 'place' in tweet_full and not tweet_full['place'] is None:
        tweet['place'] = tweet_full['place']['full_name']
    else:
        tweet['place'] = ''
    if tweet['coordinate_lat'] == -1 and tweet['coordinate_long'] == -1 and tweet['place'] == '' :
        return None
    if 'quoted_status' in tweet_full and not tweet_full['quoted_status'] is None:
        tweet['quote_id'] = tweet_full['quoted_status']['id']
    else:
        tweet['quote_id'] = -1
    return tweet


def load_tweet_jsonl(file_path, only_geo=False):
    tweets_js = pd.read_json(
        file_path,
        compression='gzip',
        encoding='utf-8',
        orient='records',
        lines=True,
        dtype={'id': np.uint64}
    )
    tweets_js: pd.DataFrame = tweets_js.dropna(subset=['id'])
    tweets_js['id'] = tweets_js['id'].map(lambda x: int(x))
    tweets_js = tweets_js.groupby('id').first().copy()
    try:
        if 'retweeted_status' in tweets_js.columns:
            tweets_js = tweets_js[tweets_js['retweeted_status'].isnull()]
        tweets_js = tweets_js[['user','created_at','text','entities','place']]
        tweets_js['user_id'] = tweets_js['user'].map(lambda x: x['id'])
        tweets_js['description'] = tweets_js['user'].map(lambda x: x['description'])
        tweets_js['location'] = tweets_js['user'].map(lambda x: x['location'])
        tweets_js['mention'] = tweets_js['entities'].map(lambda x: x['user_mentions'] if x is not None and 'user_mentions' in x else None)
        tweets_js['place'] = tweets_js['place'].map(lambda x: x['full_name'] if x is not None else None)
        tweets_geo: pd.DataFrame = tweets_js[['user_id','description','location','created_at','text','mention','place']].copy()
        if only_geo:
            tweets_geo = tweets_geo.dropna(subset=['place'])
    except Exception as e:
        print(tweets_js.columns)
        print(tweets_js['place'])
        raise e
    return tweets_geo












