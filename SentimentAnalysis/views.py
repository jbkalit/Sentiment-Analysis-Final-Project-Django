# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ClassifyForm
from .forms import SearchForm
import pandas as pd
import csv
from Algo import Classify
# Create your views here.

def upload(request):
	tweets = []
	if request.method == "POST" and request.FILES['myfile']:
		myfile = request.FILES['myfile']
		readCSV =csv.DictReader(myfile, delimiter=',')
		for row in readCSV:
			obj = {}
		  	obj['text'] = (row['text'])
		  	obj['emotion'] = (row['emotion'])
		  	df = pd.DataFrame({'text': row['text'],'emotion': row['emotion']}, index=[0])
		  	print obj
			#tweets = df
			tweets.append(obj)
	return render(request, 'SentimentAnalysis/index.html',{'tweets':tweets})

