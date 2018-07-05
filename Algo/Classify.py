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
import pkg_resources
import itertools
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report


resource_package = __name__

resource_path = '/'.join(('', 'model/svm_rbf_hp_model.pkl'))
clf_path = pkg_resources.resource_filename(resource_package, resource_path)
model = joblib.load(clf_path)

resource_path = '/'.join(('', 'model/count_vect.pkl'))
vec_path = pkg_resources.resource_filename(resource_package, resource_path)
vec = joblib.load(vec_path)

resource_path = '/'.join(('', 'model/tfidf_transformer.pkl'))
idf_path = pkg_resources.resource_filename(resource_package, resource_path)
idf = joblib.load(idf_path)

def clasification_SVM_RBF(dataframe):
    tfidf_transformer = TfidfTransformer()
    count_vect = CountVectorizer()

    data_samples = dataframe.text

    X_new_counts = vec.transform(data_samples)
    X_new_tfidf = idf.transform(X_new_counts)

    dataframe['predict'] = pd.DataFrame({'predict': model.predict(X_new_tfidf)})
    y_test = dataframe.emotion.astype(np.int64)
    predict = dataframe.predict
    
    dataframe['state'] = np.where(y_test == predict, 'matched', 'unmatched')
    accuracy = accuracy_score(y_test, predict)
    accuracy = 100 * accuracy
    conf = confusion_matrix(y_test, predict)
    report = classification_report(y_test, predict)

    return convertToDict(dataframe) , accuracy , conf, report

def findState(dataframe):
    dataframe['state']= np.where((dataframe['predict'] == 2), 'matched' , 'unmatched')
    print dataframe
    return dataframe
    

def convertToDict(tweet):
    tweets = []  
    for i in range(len(tweet)):
        obj = {}
        #print "test 2 ", tweet.loc[i]['text']
        obj['text'] = tweet.loc[i]['text']
        obj['emotion'] = tweet.loc[i]['emotion']
        obj['predict'] = tweet.loc[i]['predict']
        obj['state'] = tweet.loc[i]['state']
        #print tweet.iloc[i]['text']
        tweets.append(obj)
    return tweets

def GraphsViewBar(request):
    f = plt.figure()
    x = np.arange(10)
    h = [0,1,2,3,5,6,4,2,1,0]
    plt.title('Title')
    plt.xlim(0, 10)
    plt.ylim(0, 8)
    plt.xlabel('x label')
    plt.ylabel('y label')
    bar1 = plt.bar(x,h,width=1.0,bottom=0,color='Green',alpha=0.65,label='Legend')
    plt.legend()

    canvas = FigureCanvasAgg(f)    
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    matplotlib.pyplot.close(f)   
    return response

def analyzeInput(text):
    
    tweet = []

    tfidf_transformer = TfidfTransformer()
    count_vect = CountVectorizer()

    tweet = [text]

    X_new_counts = vec.transform(tweet)
    X_new_tfidf = idf.transform(X_new_counts)

    predict = model.predict(X_new_tfidf)

    if predict == 0:
        predict = "joy"
    elif predict == 1:
        predict = "fear"
    elif predict == 2:
        predict = "anger"
    elif predict == 3:
        predict = "sadness"
    elif predict == 4:
        predict = "disgust"
    elif predict == 5:
        predict = "surprise"

    return predict
