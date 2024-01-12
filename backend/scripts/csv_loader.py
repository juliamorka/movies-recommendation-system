from movies.models import Movie, Genre, Tag, Rating, Recommendation
import csv
import pandas as pd
from imdb import Cinemagoer
from django.contrib.auth.models import User


def run():
    # movies = pd.read_csv("data/movies.csv")
    # links = pd.read_csv("data/links.csv")
    # movies_links = movies.merge(links, on="movieId")
    # movies_links.to_csv("data/movies_links.csv", index=False)

    Rating.objects.all().delete()
    Recommendation.objects.all().delete()
    # Movie.objects.all().delete()
    # Genre.objects.all().delete()

    # with open('data/movies_links_posters.csv', errors="ignore") as file:
    #     reader = csv.reader(file)
    #     next(reader)
    #     # ia = Cinemagoer()
    #     for i, row in enumerate(reader):
    #         poster_url = "https://i.pinimg.com/736x/83/e5/04/83e504d41bffdcdebfc8e3dad72e887f.jpg" if row[6] == "empty.png" else row[6]
    #         try:
    #             film = Movie(id=row[1],
    #                          title=row[2][:40],
    #                          imdb_id=row[4],
    #                          poster_url=poster_url,
    #                          )
    #             film.save()
    #         except:
    #             print("Movie:", row[2])
    #             continue
    #         for entry in row[3].split("|"):
    #             genre, _ = Genre.objects.get_or_create(name=entry)
    #             film.genres.add(genre)

    with open('data/ratings.csv', errors="ignore") as file:
        reader = csv.reader(file)
        next(reader)

        for i, row in enumerate(reader):
            user, _ = User.objects.get_or_create(username="user"+str(row[0]),
                                                 password="password",
                                                 )
            # user.save()
            try:
                movie = Movie.objects.get(id=row[1])
            except:
                print(row[1])
                continue
            Rating.objects.create(value=float(row[2]), movie=movie, user=user)

# python manage.py runscript csv_loader
