from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Tag(models.Model):
    text = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.text


class Genre(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=40, unique=True)
    genres = models.ManyToManyField(Genre, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    imdb_id = models.IntegerField(unique=True, blank=True, null=True)
    poster_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    value = models.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    movie = models.ForeignKey(Movie, default=1, on_delete=models.PROTECT)
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)

    def __str__(self):
        return "_".join(str(self.movie).split(" ")) + "_" + str(self.user)


class Recommendation(models.Model):
    movie = models.ForeignKey(Movie, default=1, on_delete=models.PROTECT)
    user = models.ForeignKey(User, default=1, on_delete=models.PROTECT)

    def __str__(self):
        return "_".join(str(self.movie).split(" ")) + "_" + str(self.user)
