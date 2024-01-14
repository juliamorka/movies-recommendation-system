from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from movies.models import Profile
from django.db.models import Max
from django.db.models.functions import Cast
from django.db.models import IntegerField

class Login(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        return HttpResponseRedirect(redirect_to="/films")

    def post(self, request):
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if user is None:
            return HttpResponse(f"User does not exist", content_type="text/plain")
        else:
            login(request, user)
            return HttpResponseRedirect(redirect_to="/films")


class Register(APIView):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        user = User.objects.create_user(username=request.data["username"],
                                        password=request.data["password"])
        max_imdb_id = Profile.objects.annotate(imdb_id_integer=Cast('imdb_id', output_field=IntegerField())).aggregate(Max('imdb_id_integer'))['imdb_id_integer__max']
        profile = Profile.objects.create(user=user, cluster=4, imdb_id=max_imdb_id+1)
        profile.save()
        login(request, user)
        return HttpResponseRedirect(redirect_to="/recommendations")


class Logout(APIView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(redirect_to="/auth/login")
