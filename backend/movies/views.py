from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Movie, Rating, Recommendation, Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import operator

from background_task import background
from django.contrib.auth.models import User
import time

from movies.recommender_app import regenerate_recs_in_new_cluster
from recommender.apps import recommender


@background(queue="recommender")
def recalculate_recs_after_exhaustion(user_id):
    profile_id = Profile.objects.get(user=user_id).imdb_id
    regenerate_recs_in_new_cluster(profile_id, recommender)


def index(request):
    if request.user.is_authenticated:
        user_ratings = Rating.objects.filter(user=request.user)
        rated_movies_ids = [user_rating.movie.id for user_rating in user_ratings]
        movies = Movie.objects.all().exclude(id__in=rated_movies_ids).order_by('id')
        if request.GET.get('q'):
            search = request.GET.get('q')
            movies = movies.filter(title__iregex=search)
        else:
            movies = movies[:12]
        movies_urls = movies.values("poster_url")
        return render(request, 'movies.html', {"movies": zip(movies, movies_urls)})
    return HttpResponseRedirect(redirect_to="/auth/login")


class RatingsView(APIView):

    def post(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        user = request.user
        rec = Recommendation.objects.filter(user=user, movie=movie)
        Rating.objects.create(value=request.data["rating"], movie=movie, user=user)
        if rec.exists():
            rec.delete()
            if not Recommendation.objects.filter(user=user):
                recalculate_recs_after_exhaustion(user.id)
        return HttpResponseRedirect(redirect_to="/movies")
        # return Response({}, status=status.HTTP_201_CREATED)

    def delete(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        Rating.objects.filter(movie=movie, user=request.user).delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def get(self, request):
        if request.user.is_authenticated:
            user_ratings = sorted(Rating.objects.filter(user=request.user), key=operator.attrgetter('movie.title'))
            rated_movies_ids = [user_rating.movie.id for user_rating in user_ratings]
            if request.GET.get('page'):
                page_num = int(request.GET.get('page'))
            else:
                page_num = 1
            rated_movies_ids = rated_movies_ids[12 * page_num - 12:12 * page_num]
            movies = sorted(Movie.objects.filter(id__in=rated_movies_ids), key=operator.attrgetter('title'))
            movies_urls = [movie.poster_url for movie in movies]
            return render(request, 'ratings.html',
                          {"movies": zip(movies, movies_urls, user_ratings), "page": page_num})
        return HttpResponseRedirect(redirect_to="/auth/login")


class RecommendationsView(APIView):
    def get(self, request):
        user = request.user
        if request.user.is_authenticated:
            user_recs = Recommendation.objects.filter(user=request.user)
            if not user_recs:
                recalculate_recs_after_exhaustion(user.id)
            rec_movies_ids = [user_rec.movie.id for user_rec in user_recs]
            movies = sorted(Movie.objects.filter(id__in=rec_movies_ids), key=operator.attrgetter('title'))
            movies_urls = [movie.poster_url for movie in movies]
            return render(request, 'recommendations.html', {"movies": zip(movies, movies_urls)})
        return HttpResponseRedirect(redirect_to="/auth/login")
