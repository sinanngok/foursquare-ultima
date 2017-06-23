from django.db import models
from django.utils import timezone

class PreviousSearch(models.Model):
    search_key = models.CharField(max_length=200)
    search_location = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
