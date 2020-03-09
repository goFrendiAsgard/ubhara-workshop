import os
import tweepy
import psycopg2
import traceback

twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

postgres_host = os.environ['POSTGRES_HOST']
postgres_database = os.environ['POSTGRES_DATABASE']
postgres_user = os.environ['POSTGRES_USER']
postgres_password = os.environ['POSTGRES_PASSWORD']
postgres_schema = os.environ['POSTGRES_SCHEMA']

postgres_create_db_sql = 'CREATE SCHEMA IF NOT EXISTS ' + \
    postgres_schema + ';'
postgres_create_table_sql = 'CREATE TABLE IF NOT EXISTS '+postgres_schema+'.statuses ( ' + \
    '    id SERIAL PRIMARY KEY,' + \
    '    tweet_id VARCHAR(50) NOT NULL,' + \
    '    text TEXT,' + \
    '    hashtag VARCHAR(50),' + \
    '    user_id VARCHAR(50),' + \
    '    user_name VARCHAR(100),' + \
    '    retweet_count INTEGER,' + \
    '    reply_count INTEGER,' + \
    '    created_at VARCHAR(50)' + \
    ')'


def create_connection():
    return psycopg2.connect(
        host=postgres_host, user=postgres_user, password=postgres_password, dbname=postgres_database)


def create_postgres_schema():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(postgres_create_db_sql)
    cursor.execute(postgres_create_table_sql)
    cursor.close()
    connection.commit()
    connection.close()


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def on_status(self, status):
        if status.retweeted or not hasattr(status, 'extended_tweet'):
            return None
        print('ID: ', status.id_str)
        print('FULL_TEXT:', status.extended_tweet['full_text'])
        print('HASHTAGS: ', status.entities['hashtags'])
        print('USER_ID:', status.user.id_str)
        print('USER_NAME:', status.user.name)
        print('RETWEET_COUNT: ', status.retweet_count)
        print('REPLY_COUNT: ', status.reply_count)
        print('CREATED AT: ', status.created_at)
        print('======================================')
        hashtags = status.entities['hashtags']
        for hashtag in hashtags:
            hashtag_text = hashtag['text']
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO '+postgres_schema +
                '.statuses(tweet_id, text, hashtag, user_id, user_name, retweet_count, reply_count, created_at) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)',
                (status.id_str, status.extended_tweet['full_text'], hashtag_text, status.user.id_str, status.user.name, status.retweet_count, status.reply_count, status.created_at))
            cursor.close()
            connection.commit()


create_postgres_schema()

connection = create_connection()
twitter_auth = tweepy.OAuthHandler(
    twitter_consumer_key, twitter_consumer_secret)
twitter_auth.set_access_token(
    twitter_access_token, twitter_access_token_secret)
twitter_api = tweepy.API(twitter_auth)

# create stream listener
myStreamListener = MyStreamListener(connection)
myStream = tweepy.Stream(
    auth=twitter_api.auth, listener=myStreamListener, tweet_mode='extended')
myStream.filter(
    track=['a'],
    languages=['en'])
