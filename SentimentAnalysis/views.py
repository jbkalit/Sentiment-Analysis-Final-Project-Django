# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ClassifyForm
from .forms import SearchForm
import Classify as Classify
import pandas as pd
import csv
# Create your views here.

def index(request):
	#form = SearchForm()
	#form = fileForm()
	tweets = []
	#tweetSentimentPairs = []
	fileSentimentPair = []
	loadResults = False
	# if request.method == "POST":
	# 	form = SearchForm(request.POST)
	# 	if form.is_valid():
	# 		if len(str(form.cleaned_data)) > 0:
	# 			SearchTerm = str(form.cleaned_data['query'])
	# 			tweets = Classify.getTweets(100, SearchTerm)
	# 			tweetSentimentPairs = Classify.classifyTweets(tweets,SearchTerm)
	# 			loadResults = True
	if request.method == "POST" and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		#form = SearchForm(request.POST)
		#file_data = myfile.read().decode("utf-8")
		# lines = file_data.split("\n")
		# for line in file_data:
		#  	coloumn = line.split(",")
		# # 	data_dict = {}
		#  	number = coloumn[0]
		#  	text = coloumn[1]
		#  	emotion = coloumn[2]
		readCSV =csv.DictReader(myfile, delimiter=',')
		for row in readCSV:
			#print(row[1])
		  	tweets.append(row['text'])
		  	tweets.append(row['emotion'])
		# 	tweets = (data_dict)
		#coloumn = ['text', 'emotion']
		#data = pd.myfile
		#text = data['text']
		#print text
		#tweets = text
		#tweets = (data_text, data_emotion)
		print tweets

	return render(request, 'SentimentAnalysis/index.html',{'tweets':tweets})

	#return render(request,'SentimentAnalysis/index.html',{'searchForm':form,' tweets':tweets,'pairs':tweetSentimentPairs, 'loadResults':loadResults})