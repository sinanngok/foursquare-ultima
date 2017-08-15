from .models import  MyUser as User
from django.contrib.auth import authenticate
from django.utils import timezone

class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated():
            # Update last visit time before request finished processing.
            request.user.last_visit = timezone.now()
            request.user.save(update_fields=['last_visit'])
        response = self.get_response(request)
        return response
