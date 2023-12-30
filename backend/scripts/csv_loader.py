from movies.models import Movie, Genre, Tag, Rating, Recommendation
import csv
import pandas as pd
from imdb import Cinemagoer
from django.contrib.auth.models import User


def run():
    movies = pd.read_csv("data/movies.csv")
    links = pd.read_csv("data/links.csv")
    movies_links = movies.merge(links, on="movieId")
    movies_links.to_csv("data/movies_links.csv", index=False)

    Rating.objects.all().delete()
    Recommendation.objects.all().delete()
    Movie.objects.all().delete()
    Genre.objects.all().delete()

    with open('data/movies_links.csv') as file:
        reader = csv.reader(file)
        next(reader)

        for i, row in enumerate(reader):
            ia = Cinemagoer()
            poster_url = ia.get_movie(row[3])["full-size cover url"]
            film = Movie(id=row[0],
                         title=row[1],
                         imdb_id=row[3],  # niepotrzebne w sumie, tylko do Cinemagoera
                         poster_url=poster_url,
                         )
            film.save()
            for entry in row[2].split("|"):
                genre, _ = Genre.objects.get_or_create(name=entry)
                film.genres.add(genre)

    with open('data/ratings.csv') as file:
        reader = csv.reader(file)
        next(reader)

        for i, row in enumerate(reader):
            user = User(username=str(row[0]),
                        password="password",
                        )
            user.save()
            movie = Movie.objects.get(pk=row[1])
            Rating.objects.create(value=row[2], movie=movie, user=user)

# python manage.py runscript csv_loader
