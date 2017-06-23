from django import forms
from .models import PreviousSearch

class FoursquareSearchForm(forms.ModelForm):
    """search_key = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "I am looking for..."}), label='')
    search_location = forms.CharField(max_length=200, widget=forms.TextInput({ "placeholder": "Location"}), label='')
    """

    class Meta:
        model = PreviousSearch
        fields = ('search_key', 'search_location',)
        widgets = {
            'search_key': forms.TextInput({ "placeholder": "I am looking for..."}),
            'search_location': forms.TextInput({ "placeholder": "Location"}),

        }
        labels = {
            'search_key': (""),
            'search_location': (""),
        }
