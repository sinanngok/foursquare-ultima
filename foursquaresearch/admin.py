from django.core import serializers
from django.contrib.auth.models import User
from django.contrib import admin
from .models import PreviousSearch, Favorite, Place

class HistoryAdmin(admin.ModelAdmin):
    fields = ['search_key', 'search_location']
    list_display = ('user', 'search_key', 'search_location', 'created_date')
    search_fields = ('user__username', 'search_key', 'search_location', 'created_date')

admin.site.register(PreviousSearch, HistoryAdmin)

class PlaceAdmin(admin.ModelAdmin):
    fields = ['name', 'location']
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

admin.site.register(Place, PlaceAdmin)

class FavoriteAdmin(admin.ModelAdmin):
    fields = ['user', 'place']
    list_display = ('user', 'place')
    search_fields = ('user__username', 'place__name',)

admin.site.register(Favorite, FavoriteAdmin)
