from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
import requests
import json

from .models import PreviousSearch


def get_foursquare_results(location, what_to_look, venues, error, is_searched, logged_in, user):
    API_ADRESS = "https://api.foursquare.com/v2/venues/search?client_id="
    CLIENT_ID ="V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK"
    SECRET_TOKEN = "&client_secret="
    CLIENT_SECRET = "L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF"
    LOCATION_TYPE = "&near="
    proto_url = f'{API_ADRESS}{CLIENT_ID}{SECRET_TOKEN}{CLIENT_SECRET}{LOCATION_TYPE}'
        #f"My cool string is called {name}."

    #VERSION date: 20.06.2017 --> 20170620
    VERSION = "&v=20170620"
    SEARCH_PLACE = "&m=foursquare"
    post_url = f'{VERSION}{SEARCH_PLACE}'

    url = f'{proto_url}{location}&query={what_to_look}{post_url}'

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:   #checks if the location parameter is true
        venues = data["response"]["venues"]

        if venues:    #checks if there is anything found
            if logged_in:
                PreviousSearch.objects.create(user=user, search_key=what_to_look, search_location=location)
            else:
                PreviousSearch.objects.create(search_key=what_to_look, search_location=location)
            error = ""
            is_searched = True
        else:
            error = "There is nothing to show."
    else:
        error = "Location not found, please try somewhere else."

    return (location, what_to_look, venues, error, is_searched)

def get_history(logged_in, user):
    if logged_in:
        history = PreviousSearch.objects.filter(user=user.id).order_by('-created_date')
    else:
        history = PreviousSearch.objects.order_by('-created_date')

    return (history)
