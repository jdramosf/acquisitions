# acquisitions script
import os
import json
import datetime
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import settings

ckey = settings.CONSUMER_KEY
csecret = settings.CONSUMER_SECRET
atoken = settings.TOKEN_ACCESS
asecret = settings.TOKEN_SECRET

class Listener(StreamListener):

	def on_data(self, data):
		parsed = json.loads(data)
		print(json.dumps(parsed, indent = 4))
		return True

	def on_error(self, status):
		print(status, "here")

def get_tweets_by_date(user, start_date, end_date, api):
	tweets = []
	tmp_tweets = api.user_timeline(user)
	for tweet in tmp_tweets:
		if tweet.created_at < end_date and tweet.created_at > start_date:
			tweets.append(tweet)

	return tweets


if __name__ == '__main__':
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	api = tweepy.API(auth)

	# I've disabled the listener for now, since we want to look at historical data
	#twitterStream = Stream(auth, Listener())
	#twitterStream.filter(track = ["Austin"])

	start_date = datetime.datetime(2015, 1, 1, 0, 0, 0)
	end_date = datetime.datetime(2016, 1, 1, 0, 0, 0)

	tweets = get_tweets_by_date('google', start_date, end_date, api)
	print(tweets)

