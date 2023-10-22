from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout


class Login(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        return HttpResponseRedirect(redirect_to="/auth/logout")

    def post(self, request):
        user = authenticate(username=request.data["username"], password=request.data["password"])
        if user is None:
            return HttpResponse(f"User does not exist", content_type="text/plain")
        else:
            login(request, user)
            return HttpResponse(f"User exists", content_type="text/plain")


class Register(APIView):
    def post(self, request):
        return HttpResponse("Registr post")


class Logout(APIView):
    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request):
        logout(request)
        return HttpResponse("Logout")
