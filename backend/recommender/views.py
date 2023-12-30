from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(request, 'recommendations.html')
    return HttpResponseRedirect(redirect_to="/auth/login")
