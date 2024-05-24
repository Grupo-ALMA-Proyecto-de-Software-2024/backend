from django.urls import path

from . import views

urlpatterns = [
    path("carousel/", views.CarouselImageView.as_view(), name="carousel"),
    path("publications/", views.PublicationView.as_view(), name="publications"),
]
