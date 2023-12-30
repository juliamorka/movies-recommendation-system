from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# Create your views here.

class UserView(APIView):
    def get(self, request, username):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        user = User.objects.get(username=username)
        return render(request, 'user.html', {'user': user})
