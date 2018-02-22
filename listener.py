# acquisitions script
import os
import json
import datetime
import tweepy
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

	for status in tweepy.Cursor(api.user_timeline,
								id = user,
								max_id = 940636418254110720).items():
		if status.created_at < end_date and status.created_at > start_date:
			tweets.append(status)
			print("Here?")
			print(len(tweets))

	while tweets[-1].created_at > start_date:
		print("Last Tweet @", tweets[-1].created_at, "with id", tweets[-1].id, "- fetching some more")
		for status in tweepy.Cursor(api.user_timeline,
									id = user,
									max_id = tweets[-1].id - 1).items():
			if status.created_at < end_date and status.created_at > start_date:
				tweets.append(status)
				print(status.id)
				print(len(tweets))

	return len(tweets)

if __name__ == '__main__':
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	api = tweepy.API(auth)

	# I've disabled the listener for now, since we want to look at historical data
	#twitterStream = Stream(auth, Listener())
	#twitterStream.filter(track = ["Austin"])

	start_date = datetime.datetime(2017, 1, 1)
	end_date = datetime.datetime(2018, 1, 1)
	print(start_date, end_date)

	tweets = get_tweets_by_date('Google', start_date, end_date, api)
	print(tweets)

