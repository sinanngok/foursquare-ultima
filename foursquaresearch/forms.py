from django import forms
from .models import PreviousSearches

class FoursquareSearchForm(forms.Form):
    search_key = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "I am looking for..."}), label='')
    search_location = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "Location"}), label='')
