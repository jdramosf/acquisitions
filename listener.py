# acquisitions script
import os
import json
import datetime
import tweepy
import pprint
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

def get_tweets_by_date(user, api):
	for status in tweepy.Cursor(api.user_timeline,
								id = user).items():
		pprint.pprint(status._json)
		#print(json.dumps(parsed, indent = 2))

if __name__ == '__main__':
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	api = tweepy.API(auth)

	# I've disabled the listener for now, since we want to look at historical data
	#twitterStream = Stream(auth, Listener())
	#twitterStream.filter(track = ["Austin"])

	acquirees = ["the60dB", "Dialogflow", "itasoftware", "Zyncrender", "Anvato"]
	date_acquired = ["10-11-2017", "9-19-2016", "4-12-2011", "8-26-2014", "7-8-2016"]

	for acquiree in acquirees:
		get_tweets_by_date(acquiree, api)





