from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from accounts.models import MyUser as User
from .forms import RegistrationForm, UserLoginForm
from .models import Favorite, Place
from .utils import get_foursquare_results, get_history, last_active_users


def index(request):

    what_to_look = request.GET.get("look_for")
    location = request.GET.get("location")
    is_searched = False
    error_message = ''
    venues = []
    logged_in = False
    user = request.user
    favorite_list = []


    if user.is_authenticated():
        logged_in = True
        favorite_list = list(request.user.favorites.values_list('place__foursquare_id', flat=True))
    history = get_history(logged_in, user)

    if request.method == "GET":

        if what_to_look and location:
            venues, error_message, is_searched = get_foursquare_results(location, what_to_look, venues, error_message, is_searched, logged_in, user)

        return render(request, 'foursquaresearch/imlookingfor.html', {
        'history': history,
        'location': location,
        'what_to_look': what_to_look,
        'venues': venues,
        'error_message': error_message,
        'is_searched': is_searched,
        'username': user.username,
        'favorite_list':favorite_list,
        'user_id': user.id,
        'logged_in':logged_in,
        'last_active_users': last_active_users()
        })

def favorite_handler(request):
    if request.method == "POST":
        if 'add-to-favorite' in request.POST:
            foursquare_id = request.POST['id']
            name = request.POST['name']
            location = request.POST['location']
            obj, created = Place.objects.get_or_create(
                foursquare_id=foursquare_id,
                defaults={'name': name, 'location': location},
            )
            data = {
                'favorite_exist': Favorite.objects.filter(user=request.user, place=obj).exists()
            }
            if not data['favorite_exist']:
                Favorite.objects.create(user=request.user, place=obj)
            return JsonResponse(data)
        elif 'remove-from-favorite' in request.POST:
            foursquare_id = request.POST['id']
            print(foursquare_id)
            print (request.user.favorites.filter(place__foursquare_id=foursquare_id))
            request.user.favorites.filter(place__foursquare_id=foursquare_id).delete()
            data = {
                'status': True
            }

            return JsonResponse(data)
        else:
            print ("höbölö")
            return redirect('index')

@csrf_exempt
def add_to_favorites(request):

    if request.method == "POST":
        foursquare_id = request.POST['id']
        name = request.POST['name']
        location = request.POST['location']
        obj, created = Place.objects.get_or_create(
            foursquare_id=foursquare_id,
            defaults={'name':name, 'location':location},
            )
        data = {
            'favorite_exist': Favorite.objects.filter(user=request.user, place=obj).exists()
        }
        if not data['favorite_exist']:
            Favorite.objects.create(user=request.user, place=obj)
        return JsonResponse(data)

@csrf_exempt
def remove_from_favorites_while_searching(request):
    if request.method == "POST":
        foursquare_id = request.POST['id']
        print(foursquare_id)
        print (request.user.favorites.filter(place__foursquare_id=foursquare_id))
        request.user.favorites.filter(place__foursquare_id=foursquare_id).delete()
        data = {
            'status': True
        }

        return JsonResponse(data)

def remove_from_favorites(request):
    if request.method == "POST":
        place_id = request.POST['id']
        current_page = request.POST['page']
        url = f'/favorites/?page={current_page}'
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
    'username': user.username,
    'last_active_users': last_active_users()
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
            print (form.errors)
            form = RegistrationForm()
            return render(request, 'foursquaresearch/registration.html', {
            'form': form,
            })

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
