import os
import json
import datetime
import pprint
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import bigrams
from nltk import collocations
from datetime import datetime
from dateutil.parser import parse
from collections import Counter
import tweepy
import settings
import pandas
import re
import string

from textblob import TextBlob

acquirees = [
	#"DeepMindAI",
	"Dialogflow",
	"Anvato",
	"orbitera",
	"urbanengines",
	"qwiklabs",
	"kaggle",
	"bitium",
	"adxstudio",
	"SecureIslands",
	"metanautix",
	"genee_it",
	"MSRMontreal",
	"simplygon",
	"Intentsoft",
	"cloudyn_buzz",
	"Siri",
	"locationary",
	"letsembark",
	"cueup",
	"BroadMap",
	"Burstly",
	"Musicmetric",
	"faceshift",
	"HotPotatoapp",
	"dropio",
	"belugapods",
	"tagtile",
	"glanceeapp",
	"GetKarma",
	"face",
	"ParseIt"
]

def get_tweet_sentiment(tweet):
	'''
	Utility function to classify sentiment of passed tweet
	using textblob's sentiment method
	'''
	# create TextBlob object of passed tweet text
	analysis = TextBlob(tweet)
	# set sentiment
	if analysis.sentiment.polarity > 0:
		return 'positive'
	elif analysis.sentiment.polarity == 0:
		return 'neutral'
	else:
		return 'negative'

if __name__ == "__main__":
	for acquiree in acquirees:
		df = pandas.read_csv('raw_data/' + acquiree + '.csv')
		tweet_list = df['text'].tolist()

		#col = []
		cols = []
		for i in range(len(tweet_list)):
			words = tweet_list[i].split(', ')
			#col.append(get_tweet_sentiment(' '.join(tweet_list[i])))
			for word in words:
				if word[0] == '[':
					word = word[1:]
				elif word[-1] == ']':
					word = word[:-1]
				row = {}
				#print(df.get_value(i, 'created_at'))
				#print(word)
				row['user'] = df.get_value(i, 'user')
				row['created_at'] = df.get_value(i, 'created_at')
				row['word'] = word[1:-1]
				cols.append(row)

		#df.insert(0, 'sentiment', col)
		#df.to_csv('sentiment/' + acquiree + '.csv', encoding = 'utf-8')

		new_df = pandas.DataFrame(cols)
		new_df.to_csv('flat/' + acquiree + '.csv', encoding = 'utf-8')
		
