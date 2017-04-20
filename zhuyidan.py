#init_db.py
import sqlite3,json
import tweepy,datetime,time
from tweepy import OAuthHandler


conn = sqlite3.connect('tweets.db')
cur = conn.cursor()
reset = True

if reset:
    cur.execute("DROP TABLE IF EXISTS Tweets")
    cur.execute("DROP TABLE IF EXISTS Authors")
    cur.execute("DROP TABLE IF EXISTS Mentions")


statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Tweets (tweet_id TEXT, tweet_text TEXT,author_id INT, author_name TEXT, time_stamp datetime)'
cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Authors (author_id INT, username TEXT, mention_count INT)'
cur.execute(statement)


statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Mentions (tweet_id TEXT,author_id TEXT)'
cur.execute(statement)


data1 = []
tweets = []
with open('tweets.json') as data_file:
    for line in data_file:
        data1.append(json.loads(line))

def func(data):
    for i in data:
        tweet_id =i['id']
        tweet_text = i['text']
        mentioned_authors = i['entities']['user_mentions']
        author_id = i['user']['id']
        author_name = i['user']['screen_name']

        timestamp = i["created_at"]
        hash_tag_thistweet = {}

        thistweet_reocrd = (tweet_id, tweet_text,int(author_id),author_name,timestamp)
        cmd = 'INSERT INTO [Tweets] VALUES (?,?,?,?,?)'
        cur.execute(cmd, thistweet_reocrd)
        conn.commit()
        #print(thistweet_reocrd)

        for user in mentioned_authors:
            user_id = user['id']
            user_name = user['screen_name']
            thistweet_auth_reocrd = (tweet_id,user_id)
            cmd = 'INSERT INTO [Mentions] VALUES (?,?)'
            cur.execute(cmd, thistweet_auth_reocrd)
            conn.commit()

            try:
                q = 'SELECT mention_count FROM Authors WHERE author_id ='
                q+= '"'+str(user_id)+'"'
                result = cur.execute(q)
                count = result.fetchone()[0]+1
                cmd = 'UPDATE Authors SET mention_count= '
                cmd += '"'+str(count)+'"'
                cmd += ' WHERE author_id = '
                cmd+= '"'+str(user_id)+'"'
                cur.execute(cmd)
                conn.commit()
    #
            except:
                count = 1
                record = (user_id, user_name, count)
                cmd = 'INSERT INTO [Authors] VALUES (?,?,?)'
                cur.execute(cmd, record)
                conn.commit()

func(data1)

CONSUMER_KEY = 'f0QgE87FR5W7o5RzIAZo8IaE8'
CONSUMER_SECRET = 'drI32sVxbXTJQWCKymJUwskYUX5qtvZfdXVryh6wHULYst2hZE'
ACCESS_TOKEN = '3027221122-hZwjojnOVnLjks9J6FkDgkqWfRSjevNmpVK7VOx'
ACCESS_TOKEN_SECRET = 'tTDIKk4T042eodX7FNa7dXM6I6Lj1G2tnNlRRyGjlMC0u'

# Authorization setup to access the Twitter API
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)


neighbor = []
query = 'SELECT username '
query += 'FROM Authors '
query += 'ORDER BY mention_count DESC '
cur.execute(query)
for row in cur:
        if row[0]!='umsi':
            neighbor.append(row[0])
get_tweet_count = 0
for neighbor_name in neighbor:
    if get_tweet_count < 385:
        with open('neighbor.json', 'a') as json_file:
            tweets = api.user_timeline(screen_name = neighbor_name,page =1)
            for tweet in tweets:
                if tweet.created_at>datetime.datetime(2016,9,1,0,0,0):
                    get_tweet_count+=1
                    json_tweet = tweet._json # convert to JSON format
                    json_file.write(json.dumps(json_tweet))
                    json_file.write('\n')
data2= []
with open('neighbor.json') as data_file:
    for line in data_file:
        data2.append(json.loads(line))
func(data2)


conn.close()
