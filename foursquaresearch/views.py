from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse("The Ultimate Foursquare Client will be here!")

def search_bar(request):
    return render(request, 'foursquaresearch/search_bar.html', {})
