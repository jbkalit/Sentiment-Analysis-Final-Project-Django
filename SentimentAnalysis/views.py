# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ClassifyForm
from .forms import UploadForm
import pandas as pd
import csv
from Algo import Classify
from Algo import Preprocessing
# Create your views here.


def upload(request):
	form2 = ClassifyForm()
	form = UploadForm()
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
	classify = []
	removeDuplicate = []
	accuracy = " "
	conf = " "
	report = " "
	text = " "

	if request.method == "POST":
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			myfile = request.FILES['myfile']
			readCSV =csv.DictReader(myfile, delimiter=',')
			dataCSV = list(readCSV)
			df = pd.DataFrame(dataCSV, columns=['text','emotion'])
			df.to_csv('dataframe_test.csv',encoding='utf-8')
# FOR SHOW ON GUI FILE UPLOADED
			for row in dataCSV:
				obj = {}
		  		obj['text'] = (row['text'])
		  		obj['emotion'] = (row['emotion'])
				tweets.append(obj)

			classify , accuracy, conf, report = Classify.clasification_SVM_RBF(df)

		form2 = ClassifyForm(request.POST)
		if form2.is_valid():
			text = Classify.analyzeInput(form2.cleaned_data['text'])

# PREPROCESSING

			# lowercase.append(Preprocessing.lowercase(df))
			
			# lowercaseDF = pd.DataFrame([Preprocessing.lowercase(df)])
			
			# removeNumber.append(Preprocessing.removeNumber(lowercaseDF))
			
			# removeNumberDF =  pd.DataFrame([Preprocessing.removeNumber(lowercaseDF)])

			# removeUrl.append(Preprocessing.removeUrl(removeNumberDF))

			# removeUrlDF = pd.DataFrame([Preprocessing.removeUrl(removeNumberDF)])


			# removeRT.append(Preprocessing.removeRT(removeUrlDF))
			
			# removeRTDF = pd.DataFrame([Preprocessing.removeRT(removeUrlDF)])
			
			# removeAt.append(Preprocessing.removeAt(removeRTDF))
			
			# removeAtDF =  pd.DataFrame([Preprocessing.removeAt(removeRTDF)])

			# removeBadChar.append(Preprocessing.removeBadChar(removeAtDF))

			# removeBadCharDF = pd.DataFrame([Preprocessing.removeBadChar(removeAtDF)])


			# punctuation.append(Preprocessing.punctuation(removeBadCharDF))
			
			# punctuationDF = pd.DataFrame([Preprocessing.punctuation(removeBadCharDF)])
			
			# normalization.append(Preprocessing.normalization(punctuationDF))
			
			# normalizationDF =  pd.DataFrame([Preprocessing.normalization(punctuationDF)])

			# removeStopwords.append(Preprocessing.removeStopwords(normalizationDF))

			# removeStopwordsDF = pd.DataFrame([Preprocessing.removeStopwords(normalizationDF)])

			
			# stemming.append(Preprocessing.stemming(removeStopwordsDF))
			
			# stemmingDF = pd.DataFrame([Preprocessing.stemming(removeStopwordsDF)])
			
			# removeDuplicate.append(Preprocessing.removeDuplicate(stemmingDF))
			
			# removeDuplicateDF =  pd.DataFrame([Preprocessing.removeDuplicate(stemmingDF)])

# CLASSIFICATION
		
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
		'removeDuplicate' : removeDuplicate,
		'classify' : classify,
		'accuracy': accuracy,
		'conf': conf,
		'report':report,
		'ClassifyForm':form2,
		'text':text,
		'UploadForm': form})