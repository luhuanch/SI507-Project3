import tweepy
from tweepy import OAuthHandler
import json
import sqlite3
import datetime

CONSUMER_KEY = 'f0QgE87FR5W7o5RzIAZo8IaE8'
CONSUMER_SECRET = 'drI32sVxbXTJQWCKymJUwskYUX5qtvZfdXVryh6wHULYst2hZE'
ACCESS_TOKEN = '3027221122-hZwjojnOVnLjks9J6FkDgkqWfRSjevNmpVK7VOx'
ACCESS_TOKEN_SECRET = 'tTDIKk4T042eodX7FNa7dXM6I6Lj1G2tnNlRRyGjlMC0u'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
lst = []

def update_author(tweet_id, author, cur, conn):
    username = author['screen_name']
    author_id = author['id']

    select_sql = 'SELECT * FROM Authors WHERE username = ?'
    cur.execute(select_sql,(username,))
    if not cur.fetchone():
        insert_sql = 'INSERT INTO Authors(author_id, username,num_occurrences) VALUES(?, ?, ?)'
        cur.execute(insert_sql, (author_id, username, 0))
        conn.commit()

    update_sql = 'UPDATE Authors SET num_occurrences = num_occurrences + 1 WHERE username = ?'
    cur.execute(update_sql,(username,))
    conn.commit()

    map_sql = 'SELECT * FROM Mentions WHERE author_id = ? AND tweet_id = ?'
    cur.execute(map_sql, (author_id, tweet_id))
    if not cur.fetchone():
        insert_sql = 'INSERT INTO Mentions VALUES (?, ?)'
        cur.execute(insert_sql,(author_id, tweet_id))
        conn.commit()


def save_tweet(json_tweet, cur, conn):
    tweet_id = json_tweet['id']
    author = json_tweet['user']['screen_name']
    author_id = json_tweet['user']['id']
    timestamp = json_tweet['created_at']
    text = json_tweet['text']
    mentioned_author = json_tweet['entities']['user_mentions']

    select_sql = 'SELECT * FROM Tweets WHERE tweet_id = '+ str(tweet_id)
    cur.execute(select_sql)
    if not cur.fetchone():
        insert_sql = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'
        cur.execute(insert_sql,(tweet_id, author, author_id, timestamp, text))
        conn.commit()
    for author in mentioned_author:
        update_author(tweet_id,author, cur, conn)



def add_to_db():
    conn = sqlite3.connect('tweets.db')
    cur = conn.cursor()

    with open('tweets.json', 'r') as json_file:
        for line in json_file:
            # line = line.lstrip().rstrip()
            if len(line) == 0:
                continue
            json_tweet = json.loads(line)
            save_tweet(json_tweet,cur,conn)
    conn.close()

def add_mention_tweets():
    conn = sqlite3.connect('tweets.db')
    cur = conn.cursor()

def most_common_mention(cur, conn):
    select_sql = 'SELECT * FROM Authors ORDER BY num_occurrences DESC'
    r = cur.execute(select_sql)
    next(r)

    page = 1
    num_tweets = 0
    for row in r:
        if num_tweets < 386:
            tweets = api.user_timeline(screen_name = row[1],page =1)
            for tweet in tweets:
                if twee
                json_tweet = tweet._json
                save_tweet(json_tweet, cur, conn)
                num_tweets +=  1
            else:
                break
        else:
            break

with open('neighbor.json', 'a') as json_file:
    tweets = api.user_timeline(screen_name = neighbor_name,page =1)
    for tweet in tweets:
        if tweet.created_at>datetime.datetime(2016,9,1,0,0,0):
            get_tweet_count+=1
            json_tweet = tweet._json # convert to JSON format
            json_file.write(json.dumps(json_tweet))
            json_file.write('\n')


conn = sqlite3.connect('tweets.db')
cur = conn.cursor()
add_to_db()
most_common_mention(cur, conn)
