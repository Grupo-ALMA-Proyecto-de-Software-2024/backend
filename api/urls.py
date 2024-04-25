from django.urls import path

from . import views

urlpatterns = [
    path("carousel/", views.CarouselImageView.as_view(), name="carousel"),
    path("regions/", views.RegionView.as_view(), name="regions"),
    path("disks/", views.DiskView.as_view(), name="disks"),
    path("bands/", views.BandView.as_view(), name="bands"),
    path("molecules/", views.MoleculeView.as_view(), name="molecules"),
    path("data/", views.DataView.as_view(), name="data"),
]
