import os
import tweepy
import pymysql.cursors

twitter_access_token = os.environ['TWITTER_ACCESS_TOKEN']
twitter_access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

twitter_consumer_key = os.environ['TWITTER_CONSUMER_KEY']
twitter_consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

mysql_host = os.environ['MYSQL_HOST']
mysql_user = os.environ['MYSQL_USER']
mysql_password = os.environ['MYSQL_PASSWORD']
mysql_db = os.environ['MYSQL_DB']


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, connection):
        super().__init__()
        self.connection = connection

    def on_status(self, status):
        print('TEXT: ', status.text)
        print('HASHTAGS: ', status.entities['hashtags'])
        print('CREATED AT: ', status.created_at)
        print('======================================')
        text = status.text
        hashtags = status.entities['hashtags']
        created_at = status.created_at
        for hashtag in hashtags:
            with connection.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO statuses(text, hashtag, created_at) VALUES(%s, %s, %s)',
                    (text, hashtag['text'], created_at))
            connection.commit()


# create db connection
connection = pymysql.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    db=mysql_db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)

try:

    # create table
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS statuses( 
                id int(11) NOT NULL AUTO_INCREMENT, 
                text TEXT, 
                hashtag VARCHAR(255), 
                created_at VARCHAR(20),
                PRIMARY KEY(id))
            ''')
    connection.commit()

    # create twitter api
    twitter_auth = tweepy.OAuthHandler(
        twitter_consumer_key, twitter_consumer_secret)
    twitter_auth.set_access_token(
        twitter_access_token, twitter_access_token_secret)
    twitter_api = tweepy.API(twitter_auth)

    # create stream listener
    myStreamListener = MyStreamListener(connection)
    myStream = tweepy.Stream(auth=twitter_api.auth, listener=myStreamListener)
    myStream.filter(
        track=['#severeweather', '#corona', '#electionday'],
        languages=['en'])

finally:
    connection.close()
