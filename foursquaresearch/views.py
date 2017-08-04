from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
import requests
from django.http import JsonResponse

from .models import  Favorite, Place, PreviousSearch

from .forms import RegistrationForm, UserLoginForm

from .utils import get_foursquare_results, get_history

def index(request):

    what_to_look = request.GET.get("look_for")
    location = request.GET.get("location")
    is_searched = False
    error_message = ''
    venues = []
    logged_in = False
    user = request.user
    if request.user.is_authenticated():
        logged_in = True
    history = get_history(logged_in, user)
    if request.method == "GET":

        if what_to_look and location:
            location, what_to_look, venues, error_message, is_searched = get_foursquare_results(location, what_to_look, venues, error_message, is_searched, logged_in, user)

        return render(request, 'foursquaresearch/imlookingfor.html', {
        'history': history,
        'location': location,
        'what_to_look': what_to_look,
        'venues': venues,
        'error_message': error_message,
        'is_searched': is_searched,
        'logged_in': logged_in,
        'username': user.username
        })

def add_to_favorites(request):

    if request.method == "POST":
        id = request.POST['id']
        name = request.POST['name']
        location = request.POST['location']
        obj, created = Place.objects.get_or_create(
            foursquare_id=foursquare_id,
            defaults={name:name, location:location},)
        Favorite.objects.create(user=request.user, place=obj)
        return redirect('index')

def remove_from_favorites(request):
    if request.method == "POST":
        place_id = request.POST['id']
        current_page = request.POST['page']
        url = f'/favorites/?page={current_page}'
        print (current_page)
        print (url)
        request.user.favorites.filter(place__id=place_id).delete()
        return redirect(url)

def favorites(request):
    logged_in = True
    user = request.user
    history = get_history(logged_in, user)
    favorites_list = request.user.favorites.all().order_by('id')
    paginator = Paginator(favorites_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        favorites = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        favorites = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        favorites = paginator.page(paginator.num_pages)

    num_pages = range(1, favorites.paginator.num_pages+1)
    current_page = favorites.number

    return render(request, 'foursquaresearch/favorites.html', {
    'history': history,
    'num_pages': num_pages,
    'current_page': current_page,
    'favorites': favorites,
    'logged_in': logged_in,
    'username': user.username
    })

def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect('index')

    else:
        form = RegistrationForm()
        return render(request, 'foursquaresearch/registration.html', {
        'form': form,
        })

def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)

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
