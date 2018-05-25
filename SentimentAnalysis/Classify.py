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



consumerKey = "aOeKsPYiHaNogKz839cOjNcrw"
consumerSecret = "7iVB2Wrmx5HgaDpKvEpQuOvSHSEbQvLPDRYlFBLWwLU3iQN8uh"
accessToken = "456738617-OdAQgKaDCsMpv3V2Ky20lhiphIqjGDQjbrpEAJ6v"
accessTokenSecret = "LalwuqFdMEi1CgC6t4GfQvn0J50ittqllZ2Uha6W3mPX4"
auth = OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)


def getTweets(n, contains):
    """returns n tweets that contain the contains parameter, but with that string removed from the tweet for classification purposes"""
    tweets = []
    i = 0
    for tweet in tweepy.Cursor(api.search,
                           q=contains + "-filter:retweets",
                           rpp=100,
                           result_type="mixed",
                           include_entities=True,
                           lang="en").items():
        #Replace the searched term so it is not used in sentiment classification
        tweetToAdd = cleanTweet(tweet.text)
        tweets.append(tweetToAdd)
        i += 1
        if i >= n:
            break
    return tweets

def cleanTweet(tweetText):
    """Remove links and no traditional characters from a tweet"""
    #Remove links
    cleaned = re.sub(r"(?:\@|https?\://)\S+", "", tweetText)
    #Remove non-alphanumeric characters
    pattern = re.compile('\W ')
    cleaned = re.sub(pattern,"", cleaned)
    #Remove non-ascii characters
    cleaned = re.sub(r'[^\x00-\x7F]+',' ', cleaned)
    return cleaned

def word_features(words):
    stopset = list(set(stopwords.words('english')))
    for i in  range(len(stopset)):
        stopset[i] = str(stopset[i])
    feats = []
    for word in words.split():
        for stopword in stopset:
            if word != stopword:
                feats.append((word, True))
    return dict(feats)

def classifyTweets(tweets, searchTerm):
    """Returns a list of sub lists are a pair of a tweet and its sentiment"""
    fobj = open(os.path.split(os.path.abspath(__file__))[0]+'/NBC.pickle', 'rb')
    nbc = pickle.load(fobj)
    fobj.close()
    sentiment = []
    for tweet in tweets:
        #Remove the search term from the tweet before classifying it's sentiment
        toClassify = tweet
        replacePattern = re.compile(searchTerm, re.IGNORECASE)
        toClassify = replacePattern.sub("",toClassify)
        sentiment.append([tweet,nbc.classify(word_features(toClassify))])
        # uprint(tweet)
    return sentiment

def classifySentiment(text):
    """Classify the sentiment of some text"""
    fobj = open(os.path.split(os.path.abspath(__file__))[0]+'/NBC.pickle', 'rb')
    nbc = pickle.load(fobj)
    fobj.close()
    return nbc.classify(word_features(text))

def computeSentimentStats(tweetSentimentPairs):
    totalNeg = 0.0
    totalPos = 0.0
    for pair in tweetSentimentPairs:
        if(pair[0] == "negative"):
            totalNeg += 1
        elif(pair[0] == "positive"):
            totalPos += 1
    total = totalNeg+ totalPos
    if(total > 0):
        return [round(100*(totalNeg/total),2),round(100*(totalPos/total),2)]
    else:
        return ["N/A","N/A"]
