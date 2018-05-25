from django import forms
#from django import models

class SearchForm(forms.Form):
    query = forms.CharField(label ='Search for tweets containing:', max_length=70)
    
class ClassifyForm(forms.Form):
    text = forms.CharField(label = 'Enter some text to classify:',widget=forms.Textarea, max_length=140)

# class fileForm(forms.Form):
#     name = models.CharField(max_length=100)
#     file = models.FileField(upload_to="images")

# class CSVForm(forms.Form):
# 	text = forms.CharField()
#     emotion = forms.CharField()