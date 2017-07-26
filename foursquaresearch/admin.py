from django.core import serializers
from django.contrib.auth.models import User
from django.contrib import admin
from .models import PreviousSearch, Favorite, UserSearch, Place

class HistoryAdmin(admin.ModelAdmin):
    fields = ['search_key', 'search_location']
    list_display = ('search_key', 'search_location', 'created_date')

admin.site.register(PreviousSearch, HistoryAdmin)

class PlaceAdmin(admin.ModelAdmin):
    fields = ['name', 'location']
    list_display = ('name', 'location')

admin.site.register(Place, PlaceAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    fields = ['user', 'place']
    list_display = ('user', 'place')

admin.site.register(Favorite, FavoriteAdmin)

class UserSearchAdmin(admin.ModelAdmin):
    fields = ['user', 'search']
    list_display = ('user', 'search')

admin.site.register(UserSearch, UserSearchAdmin)
