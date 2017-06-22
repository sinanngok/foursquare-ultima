from django.http import HttpResponse


def index(request):
    
    return HttpResponse("The Ultimate Foursquare Client will be here!")
