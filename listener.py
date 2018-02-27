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
import re
import string


ckey = settings.CONSUMER_KEY
csecret = settings.CONSUMER_SECRET
atoken = settings.TOKEN_ACCESS
asecret = settings.TOKEN_SECRET

#nltk.download('stopwords')
#nltk.download('punkt')
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via']

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
    
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

class Listener(tweepy.StreamListener):

	def on_data(self, data):
		parsed = json.loads(data)
		print(json.dumps(parsed, indent = 4))
		return True

	def on_error(self, status):
		print(status, "here")

def tokenize(s):
    return tokens_re.findall(s)
 
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


def get_tweets_by_date(user, limit, api):
	result = []
	limit = datetime.strptime(limit, '%m-%d-%Y')
	for status in tweepy.Cursor(api.user_timeline,
								id = user).items():
		if status.created_at < limit:
			row = {}
			row['user'] = user
			row['created_at'] = status.created_at
			row['text'] = [w for w in preprocess(status.text) if w not in stop]
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

