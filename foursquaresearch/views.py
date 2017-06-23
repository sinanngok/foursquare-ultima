from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import PreviousSearch

from .forms import FoursquareSearchForm

def index(request):
        history = PreviousSearch.objects.order_by('created_date')
        form = FoursquareSearchForm()
        return render(request, 'foursquaresearch/imlookingfor.html', {'form': form}, {'history': history}, )

#def result():

def search_history(request):
    history = PreviousSearch.objects.order_by('created_date')
    return render(request, 'foursquaresearch/imlookingfor.html', {'history': history}, )
