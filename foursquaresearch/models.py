from accounts.models import  MyUser as User
from django.db import models
from django.utils import timezone

class PreviousSearch(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True,)
    search_key = models.CharField(max_length=200)
    search_location = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.search_key

class Place(models.Model):
    foursquare_id = models.CharField(max_length=200, null=True, unique=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True, related_name="favorites")
    place = models.ForeignKey('Place', on_delete=models.CASCADE,)

    class Meta:
        unique_together = ("user", "place")

    def __str__(self):
        return self.place.name
