from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class PreviousSearch(models.Model):
    search_key = models.CharField(max_length=200)
    search_location = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.search_key

class Place(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True,)
    place = models.ForeignKey('Place', on_delete=models.CASCADE,)
    def __str__(self):
        return self.place.name

class UserSearch(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True,)
    search = models.ForeignKey('PreviousSearch', on_delete=models.CASCADE,)

    def __str__(self):
        return self.search.search_key
