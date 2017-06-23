from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone


from .models import PreviousSearch

from .forms import FoursquareSearchForm

def index(request):
    if request.method == "POST":
        form = FoursquareSearchForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.created_date = timezone.now()
            history.save()
            return redirect('index')
    else:
        history = PreviousSearch.objects.order_by('created_date')
        form = FoursquareSearchForm()
        return render(request, 'foursquaresearch/imlookingfor.html', {'form': form}, {'history': history}, )

#def result():

def search_history(request):
    history = PreviousSearch.objects.order_by('created_date')
    return render(request, 'foursquaresearch/imlookingfor.html', {'history': history}, )
