from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
from nltk.corpus import stopwords
import sys
import re
from nltk import NaiveBayesClassifier
import cPickle as pickle
from nltk.corpus import stopwords
import os
import re
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import nltk 
from nltk.corpus import stopwords
import re
import string
import csv
import os
import pandas as pd
from django.conf import settings

def removeDuplicate(tweet):
	tweet=tweet[~tweet['text'].duplicated()]
	tweet=tweet.reset_index(drop=True)

	return convertToDict(tweet)

def lowercase(tweet):
	for i in range(len(tweet)):
		text = string.lower(tweet['text'].iloc[i])
    	tweet['text'].iloc[i]=text

	return convertToDict(tweet)

def removeNumber(tweet):
	pattern=r'[0-9]+'
	for i in range(len(tweet)):
		tweet['text'].iloc[i] = re.sub(pattern,'', tweet['text'].iloc[i], flags=re.MULTILINE)

	return convertToDict(tweet)

def removeUrl(tweet):
	pattern=r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*'
	for i in range(len(tweet)):
		tweet['text'].iloc[i] = re.sub(pattern,'', tweet['text'].iloc[i], flags=re.MULTILINE)

	return convertToDict(tweet)

def removeRT(tweet):
	pattern=r'rt @\w+: '
	for i in range(len(tweet)):
		tweet['text'].iloc[i] = re.sub(pattern,'', tweet['text'].iloc[i], flags=re.MULTILINE)
	
	return convertToDict(tweet)

def removeAt(tweet):
	pattern=r'@\w+ '
	for i in range(len(tweet)):
		tweet['text'].iloc[i] = re.sub(pattern,'', tweet['text'].iloc[i], flags=re.MULTILINE)

	return convertToDict(tweet)

def removeBadChar(tweet):
	pattern=r'[^A-Za-z ]'
	for i in range(len(tweet)):
		tweet['text'].iloc[i] = re.sub(pattern,'', tweet['text'].iloc[i], flags=re.MULTILINE)

	return convertToDict(tweet)

def punctuation(tweet):
	string.punctuation
	remove=string.punctuation
	for i in range(len(tweet)):
		sent=tweet['text'].iloc[i]
		kd=' '.join(word.strip(remove) for word in sent.split())
		tweet['text'].iloc[i]=kd

	return convertToDict(tweet)

def normalization(tweet):
	module_dir = os.path.dirname(__file__)
	reader = csv.reader(open(module_dir+'/corpus/normalisasi.csv', 'r'))
	d = {}
	for row in reader:
		k,v= row
    	d[string.lower(k)] = string.lower(v)
    	#print d[k]
	pat = re.compile(r"\b(%s)\b" % "|".join(d))
	for i in range(len(tweet)):
		text = string.lower(tweet['text'].iloc[i])
    	text = pat.sub(lambda m: d.get(m.group()), text)
    	#print text
    	tweet['text'].iloc[i]=text

	return convertToDict(tweet)

def removeStopwords(tweet):
	module_dir = os.path.dirname(__file__)
	reader=csv.reader(open(module_dir+'/corpus/stopword_id.csv', 'r'))
	cachedStopWords = set(stopwords.words("english"))
	#cachedStopWords.update(reader[0][:])
	for i in range(len(tweet)):
		sent=tweet['text'].iloc[i]
    	kt=" ".join([word for word in sent.split() if word not in cachedStopWords])
    	tweet['text'].iloc[i]=kt
	
	return convertToDict(tweet)

def stemming(tweet):
	factory = StemmerFactory()
	stemmer = factory.create_stemmer()
	for i in range(len(tweet)):
		sent=tweet['text'].iloc[i]
		output = stemmer.stem(sent)
		tweet['text'].iloc[i]=output

		tweet = tweet

	return convertToDict(tweet)

def convertToDict(tweet):
	
	for i in range(len(tweet)):
	 	obj = {}	
		#print "test 2 ", tweet.loc[i]['text']
	 	obj['text'] = tweet.loc[i]['text']
	 	obj['emotion'] = tweet.loc[i]['emotion']
	 	#print tweet.iloc[i]['text']
	 	#tweets.append(obj)

	return obj