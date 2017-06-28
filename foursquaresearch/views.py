from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
import requests
import json

from .models import PreviousSearch

from .forms import FoursquareSearchForm

def index(request):
    history = PreviousSearch.objects.order_by('-created_date')
    API_ADRESS = "https://api.foursquare.com/v2/venues/search?client_id="
    CLIENT_ID ="V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK"
    CLIENT_SECRET = "L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF"
    YYYYMMDD = "20170620"
    search = False

    if request.method == "POST":
        form = FoursquareSearchForm(request.POST)

        if form.is_valid():
            new_search = form.save(commit=False)
            location = new_search.search_location
            what_to_look = new_search.search_key

            url = API_ADRESS + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&near=" + location + "&query=" + what_to_look + "&v=" + YYYYMMDD + "&m=foursquare"
            response = requests.get(url)
            data = response.json()

            if data["meta"]["code"]==200:   #checks if the location parameter is true
                venues = data["response"]["venues"]

                if bool(venues):    #checks if there is anything found
                    new_search.created_date = timezone.now()
                    new_search.save()
                    error = ""
                    search = True

                else:
                    error = "There is nothing to show."

            else:
                venues = []
                error = "Location not found, please try somewhere else."

    else:
        venues = []
        form = FoursquareSearchForm()
        error = ""

    return render(request, 'foursquaresearch/imlookingfor.html', {
    'history': history,
    "venues": venues,
    'form': form,
    'error': error,
    'search': search
    })

def search_history(request):

    q = request.GET.get("q")
    location = request.GET.get("location")
    API_ADRESS = "https://api.foursquare.com/v2/venues/search?client_id="
    CLIENT_ID ="V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK"
    CLIENT_SECRET = "L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF"
    location = location
    what_to_look = q
    YYYYMMDD = "20170620"

    if q and location:
        url = "https://api.foursquare.com/v2/venues/search?client_id=" + CLIENT_ID + "&client_secret=" + CLIENT_SECRET + "&near=" + location + "&query=" + q + "&v=" + YYYYMMDD + "&m=foursquare"
        response = requests.get(url)
        data = response.json()
        venues = data["response"]["venues"]
        PreviousSearch.objects.create(search_key=q, search_location=location)


    else:
        venues = []

#    name = venues["name"]
    history = PreviousSearch.objects.order_by('-created_date')


    return render(request, 'foursquaresearch/imlookingfor.html', {
    "q":q,
    "location": location,
    "venues": venues,
    })


#    API_ADRESS = "https://api.foursquare.com/v2/venues/search?client_id="
#    CLIENT_ID ="V131V0IPODZOAI4DH0TXB0W1VF4R1QCAHASGHJI35D3KJLWK"
#    CLIENT_SECRET = "L5RZFRA1K2KPH33H12BFD3MECOJKEBIJSLP14KXYRYW3A5AF"
#    LOCATION = q
#    WHAT_TO_LOOK = location
#    YYYYMMDD = "20170620"
#
#    my_search_query = API_ADRESS + CLIENT_ID + CLIENT_SECRET + LOCATION + WHAT_TO_LOOK + YYYYMMDD + "&m=foursquare"
#
#
#
#    response = requests.GET.get(my_search_query)
#    json_data = response.json()
#
#    in_space_count = json_data["number"]
#
#
#
#
#
