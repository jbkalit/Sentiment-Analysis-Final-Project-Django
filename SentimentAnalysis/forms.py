
from django import forms
#from django import models

class ClassifyForm(forms.Form):
    text = forms.CharField(label = 'Enter some text to classify : ',widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder' : 'Input Your Sentiment', 'style':'text-align:center;'} ), max_length=140)

class UploadForm(forms.Form):
    myfile = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', 'style' :'text-align:center'}))