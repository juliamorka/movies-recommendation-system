from django.contrib.auth.models import User
from django.http import HttpResponse


def index(request):
    if request.user.is_authenticated:
        return HttpResponse(f"Hello, world. You're logged in as {request.user.username} at recommender.", content_type="text/plain")
    return HttpResponse("Hello, world. You're not logged in at recommender.")