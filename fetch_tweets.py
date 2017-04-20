import tweepy
from tweepy import OAuthHandler
import json
import sqlite3

# from lab9_config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
CONSUMER_KEY = 'f0QgE87FR5W7o5RzIAZo8IaE8'
CONSUMER_SECRET = 'drI32sVxbXTJQWCKymJUwskYUX5qtvZfdXVryh6wHULYst2hZE'
ACCESS_TOKEN = '3027221122-hZwjojnOVnLjks9J6FkDgkqWfRSjevNmpVK7VOx'
ACCESS_TOKEN_SECRET = 'tTDIKk4T042eodX7FNa7dXM6I6Lj1G2tnNlRRyGjlMC0u'

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

with open('tweets.json', 'w') as json_file:
	page = 1
	num_tweets = 0
	while True:
		tweets = api.user_timeline('umsi', page=page)
		if tweets:
			for tweet in tweets:
				if num_tweets >= 386:
					break

				json_tweet = tweet._json # convert to JSON format
				json_file.write(json.dumps(json_tweet))
				json_file.write('\n')
				num_tweets += 1
		else:
			break
		page += 1

		if num_tweets >= 386:
			break

	print ('Wrote', num_tweets, 'tweets to file.')
