#init_db.py

import sqlite3

conn = sqlite3.connect('tweets.db')

# Put code here to create the database and tables
#
# You may want to set this up so that you can also DROP or TRUNCATE tables
# as you are developing so that you can start from scratch when you need to
reset = True
conn = sqlite3.connect('tweets.db')
cur = conn.cursor()

if reset:
    cur.execute("DROP TABLE IF EXISTS Tweets")
    cur.execute("DROP TABLE IF EXISTS Authors")
    cur.execute("DROP TABLE IF EXISTS Mentions")

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Tweets (tweet_id INTEGER PRIMARY KEY, tweet_text TEXT, author_id INTEGER, author_name TEXT, time_stamp DATETIME)'
cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Authors (author_id INTEGER, username TEXT, mention_count INTEGER )'
cur.execute(statement)

statement = 'CREATE TABLE IF NOT EXISTS '
statement += 'Mentions (tweet_id INTEGER, author_id INTEGER)'
cur.execute(statement)

conn.close()
