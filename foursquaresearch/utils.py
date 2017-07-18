from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import requests
import json

from .models import PreviousSearch

from .forms import FoursquareSearchForm


def Get_Foursquare_Results(location, what_to_look, venues, error, search):
    API_ADRESS = "https://api.foursquare.com/v2/venues/search?client_id="
    CLIENT_ID ="V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK"
    SECRET_TOKEN = "&client_secret="
    CLIENT_SECRET = "L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF"
    LOCATION_TYPE = "&near="
    proto_url = ''.join([API_ADRESS, CLIENT_ID, SECRET_TOKEN, CLIENT_SECRET, LOCATION_TYPE])

    #VERSION date: 20.06.2017 --> 20170620
    VERSION = "&v=20170620"
    SEARCH_PLACE = "&m=foursquare"
    post_url = ''.join([VERSION, SEARCH_PLACE])

    url = ''.join([proto_url, location, "&query=", what_to_look, post_url])

    response = requests.get(url)
    data = response.json()

    if data["meta"]["code"]==200:   #checks if the location parameter is true
        venues = data["response"]["venues"]

        if bool(venues):    #checks if there is anything found
            PreviousSearch.objects.create(search_key=what_to_look, search_location=location)
            error = ""
            search = True

        else:
            error = "There is nothing to show."
    else:
        error = "Location not found, please try somewhere else."


    return (location, what_to_look, venues, error, search)
