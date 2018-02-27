# acquisitions script
import os
import json
import datetime
import pprint
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from datetime import datetime
from dateutil.parser import parse
import tweepy
import settings
import pandas

nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

ckey = settings.CONSUMER_KEY
csecret = settings.CONSUMER_SECRET
atoken = settings.TOKEN_ACCESS
asecret = settings.TOKEN_SECRET

class Listener(tweepy.StreamListener):

	def on_data(self, data):
		parsed = json.loads(data)
		print(json.dumps(parsed, indent = 4))
		return True

	def on_error(self, status):
		print(status, "here")

def get_tweets_by_date(user, limit, api):
	result = []
	limit = datetime.strptime(limit, '%m-%d-%Y')
	for status in tweepy.Cursor(api.user_timeline,
								id = user).items():
		if status.created_at < limit:
			row = {}
			word_tokenized = word_tokenize(status.text)
			row['user'] = user
			row['created_at'] = status.created_at
			row['text'] = ' '.join([w for w in word_tokenized if not w in stop_words])
			result.append(row)
	
	return result

if __name__ == '__main__':
	auth = tweepy.OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)

	api = tweepy.API(auth)

	# I've disabled the listener for now, since we want to look at historical data
	#twitterStream = Stream(auth, Listener())
	#twitterStream.filter(track = ["Austin"])

	acquirees = ["the60dB", "Dialogflow", "itasoftware", "Zyncrender", "Anvato"]
	date_acquired = ["10-11-2017", "9-19-2016", "4-12-2011", "8-26-2014", "7-8-2016"]

	for i in range(len(acquirees)):
		result = get_tweets_by_date(acquirees[i], date_acquired[i], api)
		df = pandas.DataFrame(result)
		df.to_csv('raw_data/' + acquirees[i] + '.csv', encoding = 'utf-8')

