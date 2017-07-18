from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import requests
import json

from .models import PreviousSearch

from .forms import FoursquareSearchForm

from .utils import Get_Foursquare_Results

def index(request):

    look_for = request.GET.get("look_for")
    location = request.GET.get("location")
    what_to_look = look_for

    search = False
    error = ''
    venues = []

    if request.method == "GET":
        if look_for and location:
            location, what_to_look, venues, error, search = Get_Foursquare_Results(location, what_to_look, venues, error, search)
            print (error)
            print (search)

        history = PreviousSearch.objects.order_by('-created_date')

        return render(request, 'foursquaresearch/imlookingfor.html', {
        'history': history,
        'venues': venues,
        'error': error,
        'search': search
        })
