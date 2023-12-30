from django.contrib import admin
from movies.models import Movie, Genre, Tag, Rating, Recommendation
# Register your models here.

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(Recommendation)