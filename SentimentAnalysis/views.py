# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ClassifyForm
from .forms import UploadForm
import pandas as pd
import csv
from Algo import Classify
from Algo import Preprocessing
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


def upload(request):
	form2 = ClassifyForm()
	form = UploadForm()
	tweets = []
	datas = []
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
	ner = []
	convertnegation = []


# VARIABLES FOR SVM

	accuracy = " "
	conf = " "
	report = " "

	text = " "
	URL = " "

	percentageEmotion = ["N/A","N/A","N/A","N/A","N/A","N/A"]

	classify = []

	countMatched = []
	countUnmatched = []
	jumlahData = []
	totalData = "0"

	DataJoy = "0"
	DataFear = "0"
	DataAnger = "0"
	DataSadness = "0"
	DataDisgust = "0"
	DataSurprise = "0"	

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

# VARIABLES FOR MLP

	accuracy_MLP = " "
	conf_MLP = " "
	report_MLP = " "

	text_MLP = " "
	URL_MLP = " "

	percentageEmotion_MLP = ["N/A","N/A","N/A","N/A","N/A","N/A"]

	classify_MLP = []

	countMatched_MLP = []
	countUnmatched_MLP = []
	jumlahData_MLP = []
	totalData_MLP = "0"

	DataJoy_MLP = "0"
	DataFear_MLP = "0"
	DataAnger_MLP = "0"
	DataSadness_MLP = "0"
	DataDisgust_MLP = "0"
	DataSurprise_MLP = "0"	

	perJoy_MLP = "0"
	perFear_MLP = "0"
	perAnger_MLP = "0"
	perSadness_MLP = "0"
	perDisgust_MLP = "0"
	perSurprise_MLP = "0"

	MJoy_MLP = "0"
	MFear_MLP = "0"
	MAnger_MLP = "0"
	MSadness_MLP = "0"
	MDisgust_MLP = "0"
	MSurprise_MLP = "0"

	UJoy_MLP = "0"
	UFear_MLP = "0"
	UAnger_MLP = "0"
	USadness_MLP = "0"
	UDisgust_MLP = "0"
	USurprise_MLP = "0"

	total_MLP = "0"

	
	if request.method == "POST":
		form = UploadForm(request.POST, request.FILES)
		if form.is_valid():
			myfile = request.FILES['myfile']
			readCSV =csv.DictReader(myfile, delimiter=',')
			dataCSV = list(readCSV)
			df = pd.DataFrame(dataCSV, columns=['text','emotion'])

# FOR SHOW ON GUI FILE UPLOADED
			for row in dataCSV:
				obj = {}
		  		obj['text'] = (row['text'])
		  		obj['emotion'] = (row['emotion'])
				tweets.append(obj)
				datas.append(obj)
#PAGINATION
			page = request.GET.get('page', 1)
			paginator = Paginator(datas, 10)
			try:
				datas = paginator.page(page)
			except PageNotAnInteger:
				datas = paginator.page(1)
			except EmptyPage:
				datas = paginator.page(paginator.num_pages)

#PREPROCESSING
			
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

# CLASSIFICATION SVM			


			dataframe, classify , accuracy, conf, report = Classify.clasification_SVM_RBF(removeDuplicateDF)

			percentageEmotion , jumlahData , totalData = Classify.evaluasiPerKelas(dataframe)

			countMatched , countUnmatched , total = Classify.evaluasiPerKelasMatchUnmatch(dataframe)

			DataJoy = jumlahData[0]
			DataFear = jumlahData[1]
			DataAnger = jumlahData[2]
			DataSadness = jumlahData[3]
			DataDisgust = jumlahData[4]
			DataSurprise = jumlahData[5]

			perJoy = percentageEmotion[0]
			perFear = percentageEmotion[1]
			perAnger = percentageEmotion[2]
			perSadness = percentageEmotion[3]
			perDisgust = percentageEmotion[4]
			perSurprise = percentageEmotion[5]

			MJoy = countMatched[0]
			MFear = countMatched[1]
			MAnger = countMatched[2]
			MSadness = countMatched[3]
			MDisgust = countMatched[4]
			MSurprise = countMatched[5]

			UJoy = countUnmatched[0]
			UFear = countUnmatched[1]
			UAnger = countUnmatched[2]
			USadness = countUnmatched[3]
			UDisgust = countUnmatched[4]
			USurprise = countUnmatched[5]

# CLASSIFICATION MLP

			
			dataframe_MLP, classify_MLP ,  accuracy_MLP, conf_MLP, report_MLP = Classify.clasification_MLP(removeDuplicateDF)

			print "SVM ", accuracy
			print "MLP ", accuracy_MLP

			percentageEmotion_MLP , jumlahData_MLP , totalData_MLP = Classify.evaluasiPerKelas(dataframe_MLP)

			countMatched_MLP , countUnmatched_MLP , total_MLP = Classify.evaluasiPerKelasMatchUnmatch(dataframe_MLP)

			DataJoy_MLP = jumlahData_MLP[0]
			DataFear_MLP = jumlahData_MLP[1]
			DataAnger_MLP = jumlahData_MLP[2]
			DataSadness_MLP = jumlahData_MLP[3]
			DataDisgust_MLP = jumlahData_MLP[4]
			DataSurprise_MLP = jumlahData_MLP[5]

			perJoy_MLP = percentageEmotion_MLP[0]
			perFear_MLP = percentageEmotion_MLP[1]
			perAnger_MLP = percentageEmotion_MLP[2]
			perSadness_MLP = percentageEmotion_MLP[3]
			perDisgust_MLP = percentageEmotion_MLP[4]
			perSurprise_MLP = percentageEmotion_MLP[5]

			MJoy_MLP = countMatched_MLP[0]
			MFear_MLP = countMatched_MLP[1]
			MAnger_MLP = countMatched_MLP[2]
			MSadness_MLP = countMatched_MLP[3]
			MDisgust_MLP = countMatched_MLP[4]
			MSurprise_MLP = countMatched_MLP[5]

			UJoy_MLP = countUnmatched_MLP[0]
			UFear_MLP = countUnmatched_MLP[1]
			UAnger_MLP = countUnmatched_MLP[2]
			USadness_MLP = countUnmatched_MLP[3]
			UDisgust_MLP = countUnmatched_MLP[4]
			USurprise_MLP = countUnmatched_MLP[5]

# PREDICT ONE INPUT

		form2 = ClassifyForm(request.POST)
		if form2.is_valid():
			text, URL = Classify.analyzeInput(form2.cleaned_data['text'])


		
	return render(request, 'SentimentAnalysis/index.html',{
		'ClassifyForm':form2,
		'UploadForm': form,

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
		'ner':ner,
		'convertnegation':convertnegation,

		'accuracy': accuracy,
		'conf': conf,
		'report':report,
		'URL':URL,
		'text':text,


		'accuracy_MLP': accuracy_MLP,
		'conf_MLP': conf_MLP,
		'report_MLP':report_MLP,
		'URL_MLP':URL_MLP,
		'text_MLP':text_MLP,

		'datas':datas,
		
# MLP
		'classify_MLP' : classify_MLP,	
		'perJoy_MLP' : perJoy_MLP,
		'perFear_MLP' : perFear_MLP,
		'perAnger_MLP' : perAnger_MLP,
		'perSadness_MLP' : perSadness_MLP,
		'perDisgust_MLP' : perDisgust_MLP,
		'perSurprise_MLP' : perSurprise_MLP,
		'dataJoy_MLP' : DataJoy_MLP,
		'dataFear_MLP' : DataFear_MLP,
		'dataAnger_MLP' : DataAnger_MLP,
		'dataSadness_MLP' : DataSadness_MLP,
		'dataDisgust_MLP' : DataDisgust_MLP,
		'dataSurprise_MLP' : DataSurprise_MLP,
		'totalData_MLP' : totalData_MLP,
		'MJoy_MLP' : MJoy_MLP,	
		'MFear_MLP' : MFear_MLP,
		'MAnger_MLP' : MAnger_MLP,
		'MSadness_MLP' : MSadness_MLP,
		'MDisgust_MLP' : MDisgust_MLP,
		'MSurprise_MLP' : MSurprise_MLP,
		'UJoy_MLP'  : UJoy_MLP,
		'UFear_MLP'  : UFear_MLP,
		'UAnger_MLP' : UAnger_MLP,
		'USadness_MLP' : USadness_MLP,
		'UDisgust_MLP' : UDisgust_MLP,
		'USurprise_MLP' : USurprise_MLP,
		'total_MLP' : total_MLP,

# SVM
		'classify' : classify,
		'perJoy' : perJoy,
		'perFear' : perFear,
		'perAnger' : perAnger,
		'perSadness' : perSadness,
		'perDisgust' : perDisgust,
		'perSurprise' : perSurprise,
		'dataJoy' : DataJoy,
		'dataFear' : DataFear,
		'dataAnger' : DataAnger,
		'dataSadness' : DataSadness,
		'dataDisgust' : DataDisgust,
		'dataSurprise' : DataSurprise,
		'totalData' : totalData,
		'MJoy' : MJoy	,	
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