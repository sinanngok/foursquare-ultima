from .models import  MyUser as User
from django.contrib.auth import authenticate
from django.utils import timezone

class SetLastVisitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated():
            # Update last visit time before request finished processing.
            user = User.objects.get(pk=request.user.pk)
            user.last_visit = timezone.now()
            user.save()
        response = self.get_response(request)
        return response
