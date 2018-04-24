# acquisitions script
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


ckey = settings.CONSUMER_KEY
csecret = settings.CONSUMER_SECRET
atoken = settings.TOKEN_ACCESS
asecret = settings.TOKEN_SECRET

#nltk.download('stopwords')
#nltk.download('punkt')
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'us', '...', '…', '’']

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
    for status in tweepy.Cursor(api.user_timeline, id = user).items():
        if status.created_at < limit:
            row = {}
            row['user'] = user
            row['created_at'] = status.created_at
            pre = preprocess(status.text, lowercase=True)
            words = []
            for w in pre:
                if (w not in stop) and (user.lower() not in w) and ('http' not in w):
                    words.append(w)
                elif (user.lower() in w):
                    #print(w)
                    words.append("<SELF>")
            row['text'] = words
            result.append(row)

    return result

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    api = tweepy.API(auth)

    # I've disabled the listener for now, since we want to look at historical data
    #twitterStream = Stream(auth, Listener())
    #twitterStream.filter(track = ["Austin"])

    # Not including DeepMindAI because it doesn't return any results
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
    date_acquired = [
        #"1-26-2014",
        "9-19-2016",
        "7-8-2016",
        "8-8-2016",
        "9-15-2016",
        "11-21-2016",
        "3-8-2017",
        "9-26-2017",
        "9-28-2015",
        "11-9-2015",
        "12-18-2015",
        "8-20-2016",
        "1-13-2017",
        "1-17-2017",
        "4-18-2017",
        "6-28-2017",
        "4-27-2010",
        "7-19-2013",
        "8-22-2013",
        "10-3-2013",
        "12-23-2013",
        "2-21-2014",
        "1-21-2015",
        "11-1-2015",
        "8-20-2010",
        "10-29-2010",
        "3-2-2011",
        "4-13-2012",
        "5-5-2012",
        "5-21-2012",
        "6-18-2012",
        "4-25-2013"
    ]

    acquirers = [
        #"Google",
        "Google",
        "Google",
        "Google",
        "Google",
        "Google",
        "Google",
        "Google",
        "Microsoft",
        "Microsoft",
        "Microsoft",
        "Microsoft",
        "Microsoft",
        "Microsoft",
        "Microsoft",
        "Microsoft",
        "Apple",
        "Apple",
        "Apple",
        "Apple",
        "Apple",
        "Apple",
        "Apple",
        "Apple",
        "Facebook",
        "Facebook",
        "Facebook",
        "Facebook",
        "Facebook",
        "Facebook",
        "Facebook",
        "Facebook",
    ]

    for i in range(len(acquirees)):
        result = get_tweets_by_date(acquirees[i], date_acquired[i], api)
        df = pandas.DataFrame(result)
        df.to_csv('raw_data/' + acquirees[i] + '.csv', encoding = 'utf-8')

        # Term frequency
        count_all = Counter()
        tweet_list = df['text'].tolist()
        """
        for tweet in tweet_list:
            count_all.update(tweet)
        print(acquirees[i], count_all.most_common(5))
        """

        # Bigrams
        all_term_bigrams = []
        for tweet in tweet_list:
            term_bigrams = list(bigrams(tweet))
            #print(term_bigrams)
            for term in term_bigrams:
                #print(term)
                all_term_bigrams.append(term)

        frequencies = Counter()
        frequencies.update(all_term_bigrams)
        top_20 = (frequencies.most_common(20))
        bigram_analysis = []
        for bigram in top_20:
            row = {}
            row['word_1'] = bigram[0][0]
            row['word_2'] = bigram[0][1]
            row['count'] = bigram[1]
            row['user'] = acquirees[i]
            row['source'] = acquirers[i]
            bigram_analysis.append(row)
        bi_df = pandas.DataFrame(bigram_analysis)
        bi_df.to_csv('analysis/' + acquirees[i] + '.csv', encoding = 'utf-8')
        print(acquirees[i], 'done')

        