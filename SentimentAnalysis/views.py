# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ClassifyForm
from .forms import SearchForm
import pandas as pd
import csv
from Algo import Classify
from Algo import Preprocessing
# Create your views here.

def upload(request):
	tweets = []

	lowercase = []
	removeNumber = []
	removeUrl = []
	removeRT = []
	removeAt = []
	removeBadChar = []
	punctuation = []
	normalization = []
	removeStopwords = []
	stemming = []
	
	removeDuplicate = []


	if request.method == "POST" and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		readCSV =csv.DictReader(myfile, delimiter=',')
		
		for row in readCSV:
			obj = {}
		  	#print "test 1 ",row['text']
		  	obj['text'] = (row['text'])
		  	obj['emotion'] = (row['emotion'])
		  	df = pd.DataFrame({'text': row['text'],'emotion': row['emotion']}, index=[0])
			tweets.append(obj)
			
			#PREPROCESSING
			
			lowercase.append(Preprocessing.lowercase(df))
			
			lowercaseDF = pd.DataFrame([Preprocessing.lowercase(df)])
			
			removeNumber.append(Preprocessing.removeNumber(lowercaseDF))
			
			removeNumberDF =  pd.DataFrame([Preprocessing.removeNumber(lowercaseDF)])

			removeUrl.append(Preprocessing.removeUrl(removeNumberDF))

			removeUrlDF = pd.DataFrame([Preprocessing.removeUrl(removeNumberDF)])


			removeRT.append(Preprocessing.removeRT(removeUrlDF))
			
			removeRTDF = pd.DataFrame([Preprocessing.removeRT(removeUrlDF)])
			
			removeAt.append(Preprocessing.removeAt(removeRTDF))
			
			removeAtDF =  pd.DataFrame([Preprocessing.removeAt(removeRTDF)])

			removeBadChar.append(Preprocessing.removeBadChar(removeAtDF))

			removeBadCharDF = pd.DataFrame([Preprocessing.removeBadChar(removeAtDF)])


			punctuation.append(Preprocessing.punctuation(removeBadCharDF))
			
			punctuationDF = pd.DataFrame([Preprocessing.punctuation(removeBadCharDF)])
			
			normalization.append(Preprocessing.normalization(punctuationDF))
			
			normalizationDF =  pd.DataFrame([Preprocessing.normalization(punctuationDF)])

			removeStopwords.append(Preprocessing.removeStopwords(normalizationDF))

			removeStopwordsDF = pd.DataFrame([Preprocessing.removeStopwords(normalizationDF)])

			
			stemming.append(Preprocessing.stemming(removeStopwordsDF))
			
			stemmingDF = pd.DataFrame([Preprocessing.stemming(removeStopwordsDF)])
			
			removeDuplicate.append(Preprocessing.removeDuplicate(stemmingDF))
			
			removeDuplicateDF =  pd.DataFrame([Preprocessing.removeDuplicate(stemmingDF)])


			#cLASSIFICATION

			

	return render(request, 'SentimentAnalysis/index.html',{
		'tweets':tweets,
		'lowercase':lowercase,
		'removeNumber':removeNumber,
		'removeUrl':removeUrl,
		'removeRT' : removeRT,
		'removeAt' :  removeAt,
		'removeBadChar' : removeBadChar,
		'punctuation' : punctuation,
		'normalization' : normalization,
		'removeStopwords' : removeStopwords,
		'stemming' : stemming,
		'removeDuplicate' : removeDuplicate})

