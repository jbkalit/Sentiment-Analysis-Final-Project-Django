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

resource_path = '/'.join(('', 'model/svm.pkl'))
svm_path = pkg_resources.resource_filename(resource_package, resource_path)
model_svm = joblib.load(svm_path)

resource_path = '/'.join(('', 'model/mlp.pkl'))
mlp_path = pkg_resources.resource_filename(resource_package, resource_path)
model_mlp = joblib.load(mlp_path)

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

    dataframe['predict'] = pd.DataFrame({'predict': model_svm.predict(X_new_tfidf)})
    y_test = dataframe.emotion.astype(np.int64)
    predict = dataframe.predict
    
    dataframe['state'] = np.where(y_test == predict, 'matched', 'unmatched')
    accuracy = accuracy_score(y_test, predict)
    accuracy = 100 * accuracy
    conf = confusion_matrix(y_test, predict)
    report = classification_report(y_test, predict)

    
    return dataframe, convertToDict(dataframe) , accuracy , conf, report   

def clasification_MLP(dataframe):
    tfidf_transformer = TfidfTransformer()
    count_vect = CountVectorizer()

    data_samples = dataframe.text

    X_new_counts = vec.transform(data_samples)
    X_new_tfidf = idf.transform(X_new_counts)

    dataframe['predict'] = pd.DataFrame({'predict': model_mlp.predict(X_new_tfidf)})
    y_test = dataframe.emotion.astype(np.int64)
    predict = dataframe.predict
    
    dataframe['state'] = np.where(y_test == predict, 'matched', 'unmatched')
    accuracy_MLP = accuracy_score(y_test, predict)
    accuracy_MLP = 100 * accuracy_MLP
    conf = confusion_matrix(y_test, predict)
    report = classification_report(y_test, predict)

    return dataframe, convertToDict(dataframe), accuracy_MLP, conf, report 


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
    URL = ['']
    tfidf_transformer = TfidfTransformer()
    count_vect = CountVectorizer()

    tweet = [text]

    X_new_counts = vec.transform(tweet)
    X_new_tfidf = idf.transform(X_new_counts)

    predict = model_svm.predict(X_new_tfidf)

    #accuracy = accuracy_score(y_test, predict)
    #accuracy = 100 * accuracy

    #print accuracy

    if predict == 0:
        predict = " JOY"
        URL = '/static/images/0.png'
    elif predict == 1:
        predict = " FEAR"
        URL = '/static/images/1.png'
    elif predict == 2:
        predict = " ANGER"
        URL = '/static/images/2.png'
    elif predict == 3:
        predict = " SADNESS"
        URL = '/static/images/3.png'
    elif predict == 4:
        predict = " DISGUST"
        URL = '/static/images/4.png'
    elif predict == 5:
        predict = " SURPRISE"
        URL = '/static/images/5.png'

    return predict, URL

def evaluasiPerKelas(tweet):


    totJoy = 0.0
    totFear = 0.0
    totAnger = 0.0
    totSadness = 0.0
    totDisgust = 0.0
    totSurprise = 0.0

    listTweet = tweet['predict'].astype(np.int64)

    #print listTweet

    for pair in listTweet:
        if (pair == 0):
            totJoy += 1
        elif (pair == 1):
            totFear += 1
        elif (pair == 2):
            totAnger += 1
        elif (pair == 3):
            totSadness += 1
        elif (pair == 4):
            totDisgust += 1
        elif (pair == 5):
            totSurprise += 1

    total = totJoy + totFear + totAnger + totSadness + totDisgust + totSurprise

    if(total > 0):
        return [round(100*(totJoy/total),6),round(100*(totFear/total),6),round(100*(totAnger/total),6),round(100*(totSadness/total),6),round(100*(totDisgust/total),6),round(100*(totSurprise/total),6)] , [int(totJoy) , int(totFear) , int(totAnger) , int(totSadness) , int(totDisgust) , int(totSurprise)] , int(total)
    else:
        return ["N/A","N/A","N/A","N/A","N/A","N/A"]

def evaluasiPerKelasMatchUnmatch(tweet):

    total = 0

    MJoy = 0
    MFear = 0
    MAnger = 0
    MSadness = 0
    MDisgust = 0
    MSurprise = 0

    UJoy = 0
    UFear = 0
    UAnger = 0
    USadness = 0
    UDisgust = 0
    USurprise = 0

    predict = tweet['predict'].astype(np.int64)    
    emotion = tweet['emotion'].astype(np.int64)
    state = tweet['state'].astype(str)

    for i in range(len(tweet)):
        if predict.iloc[i] == 0 and state.iloc[i] == "matched" :
            MJoy += 1
        elif predict.iloc[i] == 1 and state.iloc[i] == "matched" :
            MFear += 1
        elif predict.iloc[i] == 2 and state.iloc[i] == "matched" :
            MAnger += 1
        elif predict.iloc[i] == 3 and state.iloc[i] == "matched" :
            MSadness += 1
        elif predict.iloc[i] == 4 and state.iloc[i] == "matched" :
            MDisgust += 1
        elif predict.iloc[i] == 5 and state.iloc[i] == "matched" :
            MSurprise += 1

    for i in range(len(tweet)):
        if predict.iloc[i] == 0 and state.iloc[i] == "unmatched" :
            UJoy += 1
        elif predict.iloc[i] == 1 and state.iloc[i] == "unmatched" :
            UFear += 1
        elif predict.iloc[i] == 2 and state.iloc[i] == "unmatched" :
            UAnger += 1
        elif predict.iloc[i] == 3 and state.iloc[i] == "unmatched" :
            USadness += 1
        elif predict.iloc[i] == 4 and state.iloc[i] == "unmatched" :
            UDisgust += 1
        elif predict.iloc[i] == 5 and state.iloc[i] == "unmatched" :
            USurprise += 1

    total = MJoy+MFear+MAnger+MSadness+MDisgust+MSurprise + UJoy+UFear+UAnger+USadness+UDisgust+USurprise

    return [MJoy,MFear,MAnger,MSadness,MDisgust,MSurprise] , [UJoy,UFear,UAnger,USadness,UDisgust,USurprise] , total
