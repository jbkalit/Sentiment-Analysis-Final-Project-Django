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
	ner = []
	convertnegation = []
	accuracy = " "
	conf = " "
	report = " "
	text = " "
	URL = " "

	percentageEmotion = ["N/A","N/A","N/A","N/A","N/A","N/A"]

	countMatched = []
	countUnmatched = []

	perJoy = "0"
	perFear = "0"
	perAnger = "0"
	perSadness = "0"
	perDisgust = "0"
	perSurprise = "0"

	MJoy = "0"
	MFear = "0"
	MAnger = "0"
	MSadness = "0"
	MDisgust = "0"
	MSurprise = "0"

	UJoy = "0"
	UFear = "0"
	UAnger = "0"
	USadness = "0"
	UDisgust = "0"
	USurprise = "0"

	total = "0"

	if request.method == "POST":
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			myfile = request.FILES['myfile']
			readCSV =csv.DictReader(myfile, delimiter=',')
			dataCSV = list(readCSV)
			df = pd.DataFrame(dataCSV, columns=['text','emotion'])
			#df.to_csv('dataframe_test.csv',encoding='utf8')
# FOR SHOW ON GUI FILE UPLOADED
			for row in dataCSV:
				obj = {}
		  		obj['text'] = (row['text'])
		  		obj['emotion'] = (row['emotion'])
				tweets.append(obj)
				#print tweets
			lowercase = Preprocessing.lowercase(df)
			
			lowercaseDF = pd.DataFrame(lowercase)
			
			removeNumber = Preprocessing.removeNumber(lowercaseDF)
			
			removeNumberDF =  pd.DataFrame(removeNumber)

			removeUrl = Preprocessing.removeUrl(removeNumberDF)

			removeUrlDF = pd.DataFrame(removeUrl)


			removeRT=(Preprocessing.removeRT(removeUrlDF))
			
			removeRTDF = pd.DataFrame(removeRT)
			
			removeAt=(Preprocessing.removeAt(removeRTDF))
			
			removeAtDF =  pd.DataFrame(removeAt)

			removeBadChar=(Preprocessing.removeBadChar(removeAtDF))

			removeBadCharDF = pd.DataFrame(removeBadChar)


			punctuation=(Preprocessing.punctuation(removeBadCharDF))
			
			punctuationDF = pd.DataFrame(punctuation)
			
			normalization=(Preprocessing.normalization(punctuationDF))

			normalizationDF =  pd.DataFrame(normalization)

			ner=(Preprocessing.NER(normalizationDF))

			nerDF =  pd.DataFrame(ner)
			

			convertnegation =(Preprocessing.convertNegation(nerDF))

			convertnegationDF =  pd.DataFrame(convertnegation)

			removeStopwords=(Preprocessing.removeStopwords(convertnegationDF))

			removeStopwordsDF = pd.DataFrame(removeStopwords)

			
			stemming=(Preprocessing.stemming(removeStopwordsDF))
			
			stemmingDF = pd.DataFrame(stemming)
			
			removeDuplicate = (Preprocessing.removeDuplicate(stemmingDF))
			
			removeDuplicateDF =  pd.DataFrame(removeDuplicate)

			dataframe, classify , accuracy, conf, report = Classify.clasification_SVM_RBF(removeDuplicateDF)

			percentageEmotion = Classify.evaluasiPerKelas(dataframe)

			countMatched , countUnmatched , total = Classify.evaluasiPerKelasMatchUnmatch(dataframe)

			perJoy = percentageEmotion[0]
			perFear = percentageEmotion[1]
			perAnger = percentageEmotion[2]
			perSadness = percentageEmotion[3]
			perDisgust = percentageEmotion[4]
			perSurprise = percentageEmotion[5]

			MJoy = countMatched[0]
			MFear = countMatched[1]
			MAnger = countMatched[2]
			Sadness = countMatched[3]
			MDisgust = countMatched[4]
			MSurprise = countMatched[5]

			UJoy = countUnmatched[0]
			UFear = countUnmatched[1]
			UAnger = countUnmatched[2]
			USadness = countUnmatched[3]
			UDisgust = countUnmatched[4]
			USurprise = countUnmatched[5]

		form2 = ClassifyForm(request.POST)
		if form2.is_valid():
			text, URL = Classify.analyzeInput(form2.cleaned_data['text'])

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
		'ner':ner,
		'convertnegation':convertnegation,
		'URL':URL,
		'UploadForm': form,
		'perJoy' : perJoy,
		'perFear' : perFear,
		'perAnger' : perAnger,
		'perSadness' : perSadness,
		'perDisgust' : perDisgust,
		'perSurprise' : perSurprise,
		'MJoy' : MJoy,
		'MFear' : MFear,
		'MAnger' : MAnger,
		'MSadness' : MSadness,
		'MDisgust' : MDisgust,
		'MSurprise' : MSurprise,
		'UJoy'  : UJoy,
		'UFear'  : UFear,
		'UAnger' : UAnger,
		'USadness' : USadness,
		'UDisgust' : UDisgust,
		'USurprise' : USurprise,
		'total' : total})