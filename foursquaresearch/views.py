from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .models import PreviousSearches

from .forms import FoursquareSearchForm

"""def search_bar(request):

    #form = NameForm()
    #return render(request, 'foursquaresearch/name.html', {'form': form})

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = FoursquareSearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = FoursquareSearchForm()

    return render(request, 'foursquaresearch/imlookingfor.html', {'form': form})

def index(request):
    return HttpResponse("The Ultimate Foursquare Client will be here!")"""

def search_bar(request):

        previous_searches = PreviousSearches.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
        form = FoursquareSearchForm()
        return render(request, 'foursquaresearch/imlookingfor.html', {'form': form}, {'previous_searches': previous_searches})
