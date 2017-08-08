from .models import  MyUser as User
from django.contrib.auth import authenticate
from django.utils import timezone

class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        if request.user.is_authenticated():
            # Update last visit time after request finished processing.
            user = User.objects.get(pk=request.user.pk)
            print("1")
            user.last_visit = timezone.now()
            print("2")

        return response
