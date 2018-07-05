
from django import forms
#from django import models

class ClassifyForm(forms.Form):
    text = forms.CharField(label = 'Enter some text to classify : ',widget=forms.Textarea, max_length=140)

class UploadForm(forms.Form):
    myfile = forms.FileField(widget=forms.FileInput(attrs={'class': 'myfieldclass', 'style' :'text-align:center'}))