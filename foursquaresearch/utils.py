from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.sessions.models import Session
from django.utils import timezone
import requests
import json

from .models import PreviousSearch
from accounts.models import  MyUser as User

def get_foursquare_results(location, what_to_look, venues, error_message, is_searched, logged_in, user):
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
            error_message = ""
            is_searched = True
        else:
            error_message = "There is nothing to show."
    else:
        error_message = "Location not found, please try somewhere else."

    return (location, what_to_look, venues, error_message, is_searched)

def get_history(logged_in, user):
    if logged_in:
        history = PreviousSearch.objects.filter(user=user.id).order_by('-created_date')[:5]
    else:
        history = PreviousSearch.objects.order_by('-created_date')[:5]

    return (history)

def get_all_logged_in_users():
    # Query all non-expired sessions
    # use timezone.now() instead of datetime.now() in latest versions of Django
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    uid_list = []

    # Build a list of user ids from that query
    for session in sessions:
        data = session.get_decoded()
        uid_list.append(data.get('_auth_user_id', None))

    # Query all logged in users based on id list
    return User.objects.filter(id__in=uid_list)

def last_active_users():
    active_users = []
    users = User.objects.order_by('-last_visit')
    for user in users:
        if user.was_active_recently():
            active_users += {user.username}
    return active_users
