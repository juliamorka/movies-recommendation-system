from django.urls import path

from . import views

urlpatterns = [
    path("films", views.index),
    path("ratings", views.RatingsView.as_view(), name="ratings"),
    path("ratings/<int:movie_id>", views.RatingsView.as_view(), name="rate"),
    path("recommendations", views.RecommendationsView.as_view(), name="recommendations")
]