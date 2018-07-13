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
import pandas as pd
import string
from bs4 import BeautifulSoup
import pkg_resources

resource_package = __name__

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

	resource_path = '/'.join(('', 'corpus/normalisasi.csv'))
	norm_path = pkg_resources.resource_filename(resource_package, resource_path)

	reader = csv.reader(open(norm_path, 'r'))

	d = {}
	for row in reader:
		k,v= row
		d[string.lower(k)] =string.lower(v)
	print "reader : ", d

	pat = re.compile(r"\b(%s)\b" % "|".join(d))
	for i in range(len(tweet)):
		text = string.lower(tweet['text'].iloc[i])
		norm = pat.sub(lambda m: d.get(m.group()), text)
		#print text
		tweet['text'].iloc[i]=norm
	
	print tweet['text']
	return convertToDict(tweet)

def removeStopwords(tweet):
	
	resource_path = '/'.join(('', 'corpus/stopword_id.xls'))
	stop_path = pkg_resources.resource_filename(resource_package, resource_path)

	reader=pd.read_excel(stop_path,header=None)
	cachedStopWords = set(stopwords.words("english"))
	cachedStopWords.update(reader[0][:])

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


def NER(data_train):
	resource_path = '/'.join(('', 'corpus/NER_evaluasi.txt'))
	NER_path = pkg_resources.resource_filename(resource_package, resource_path)

	with open(NER_path, 'r') as myfile: data=myfile.read().replace('\n', '')
	
	htmltxt = data
	soup = BeautifulSoup(htmltxt, 'lxml')
	person = soup.select('person')
	location = soup.select('location')
	time = soup.select('time')
	organization = soup.select('organization')

	persons = []
	locations = []
	times = []
	organizations = []

	for i in person:
		i = i.get_text().lower()
		persons.append(i)

	for i in location:
		i = i.get_text().lower()
		locations.append(i)

	for i in time:
		i = i.get_text().lower()
		times.append(i)

	for i in organization:
		i = i.get_text().lower()
		organizations.append(i)


	person = {'person': persons}
	personsDF = pd.DataFrame(data=person)
	personsDF.to_csv('NER_PERSON.csv',encoding='utf-8')

	location = {'location': locations}
	locationsDF = pd.DataFrame(data=location)
	locationsDF.to_csv('NER_LOCATION.csv',encoding='utf-8')

	time = {'time': times}
	timesDF = pd.DataFrame(data=time)
	timesDF.to_csv('NER_TIME.csv',encoding='utf-8')

	organization = {'organization': organizations}
	organizationsDF = pd.DataFrame(data=organization)
	organizationsDF.to_csv('NER_ORGANIZATION.csv',encoding='utf-8')

	for i in range(len(data_train)):
		if data_train['text'].iloc[i]:
			sent=data_train['text'].iloc[i]
			kt=" ".join([word for word in sent.split() if word not in persons])
			data_train['text'].iloc[i]=kt

	for i in range(len(data_train)):
		if data_train['text'].iloc[i]:
			sent=data_train['text'].iloc[i]
			kt=" ".join([word for word in sent.split() if word not in locations])
			data_train['text'].iloc[i]=kt

	for i in range(len(data_train)):
		if data_train['text'].iloc[i]:
			sent=data_train['text'].iloc[i]
			kt=" ".join([word for word in sent.split() if word not in times])
			data_train['text'].iloc[i]=kt

	for i in range(len(data_train)):
		if data_train['text'].iloc[i]:
			sent=data_train['text'].iloc[i]
			kt=" ".join([word for word in sent.split() if word not in organizations])
			data_train['text'].iloc[i]=kt

	return convertToDict(data_train)

def convertNegation(tweet):
	resource_path = '/'.join(('', 'corpus/convert_negation_id.csv'))
	cn_path = pkg_resources.resource_filename(resource_package, resource_path)

	reader = csv.reader(open(cn_path, 'r'))
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

def convertToDict(tweet):
	tweets = []  
	for i in range(len(tweet)):
		obj = {}
        #print "test 2 ", tweet.loc[i]['text']
		obj['text'] = tweet.loc[i]['text']
		obj['emotion'] = tweet.loc[i]['emotion']
       	#obj['predict'] = tweet.loc[i]['predict']
        #obj['state'] = tweet.loc[i]['state']
        #print tweet.iloc[i]['text']
		tweets.append(obj)
	return tweets
