from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
import requests

from .models import  Favorite, Place, PreviousSearch

from .forms import RegistrationForm, UserLoginForm

from .utils import get_foursquare_results, get_history

def index(request):

    look_for = request.GET.get("look_for")
    location = request.GET.get("location")
    what_to_look = look_for
    is_searched = False
    error = ''
    venues = []
    logged_in = False
    user = request.user
    if request.user.is_authenticated():
        logged_in = True
    history = get_history(logged_in, user)

    if request.method == "GET":

        if look_for and location:
            location, what_to_look, venues, error, is_searched = get_foursquare_results(location, what_to_look, venues, error, is_searched, logged_in, user)

        return render(request, 'foursquaresearch/imlookingfor.html', {
        'history': history,
        'location': location,
        'what_to_look': what_to_look,
        'venues': venues,
        'error': error,
        'is_searched': is_searched,
        'logged_in': logged_in,
        'username': user.username
        })

def add_to_favorites(request):

    if request.method == "POST":
        name = request.POST['name']
        location = request.POST['location']
        obj, created = Place.objects.get_or_create(name=name, location=location)
        Favorite.objects.create(user=request.user, place=obj)

        return redirect('index')

def remove_from_favorites(request):

    if request.method == "POST":
        place_id = request.POST['id']
        Favorite.objects.filter(user=request.user, place=Place.objects.filter(id=place_id)).delete()
        return redirect('favorites')

def favorites(request):
    logged_in = True
    user = request.user
    history = get_history(logged_in, user)
    favorites_list = Favorite.objects.filter(user=request.user)
    paginator = Paginator(favorites_list, 3) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        favorites = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        favorites = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        favorites = paginator.page(paginator.num_pages)

    return render(request, 'foursquaresearch/favorites.html', {
    'history': history,
    'favorites': favorites,
    'logged_in': logged_in,
    'username': user.username
    })

def listing(request):
    favorites_list = Favorite.objects.filter(user=request.user)
    paginator = Paginator(favorites_list, 10) # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        favorites = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        favorites = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        favorites = paginator.page(paginator.num_pages)

    return render(request, 'list.html', {'favorites': favorites})


def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('login_view')

    else:
        form = RegistrationForm()
        return render(request, 'foursquaresearch/registration.html', {
        'form': form,
        })

def login_view(request):
    form = UserLoginForm(request.POST)
    error_message = ""
    if request.method == "POST":

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

        error_message = "Please enter the correct username and password. Note that both fields may be case-sensitive."

    form = UserLoginForm()
    return render(request, 'foursquaresearch/login.html', {
    'form': form,
    'error_message': error_message,
    })

def logout_view(request):
    logout(request)
    return redirect('index')
