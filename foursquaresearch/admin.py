from django.contrib import admin
from .models import PreviousSearch

class HistoryAdmin(admin.ModelAdmin):
    fields = ['search_key', 'search_location']

    list_display = ('search_key', 'search_location', 'created_date')

admin.site.register(PreviousSearch, HistoryAdmin)
