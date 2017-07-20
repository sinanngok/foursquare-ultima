from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
import requests
import json

from .models import PreviousSearch

from .forms import RegistrationForm, UserLoginForm

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
        'location': location,
        'what_to_look': what_to_look,
        'venues': venues,
        'error': error,
        'search': search
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
            return redirect('login_view')

    else:
        form = RegistrationForm()
        return render(request, 'foursquaresearch/registration.html', {
        'form': form,
        })

def login_view(request):
    form = UserLoginForm(request.POST)
    if request.method == "POST":

        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

    else:
        form = UserLoginForm()
        return render(request, 'foursquaresearch/login.html', {
        'form': form,
        })
