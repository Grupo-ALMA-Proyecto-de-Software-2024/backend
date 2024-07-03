from django.urls import path

from .download_script_generator.controller import DownloadScriptGeneratorView
from . import views

urlpatterns = [
    path("regions/", views.RegionView.as_view(), name="regions"),
    path("disks/", views.DiskView.as_view(), name="disks"),
    path("bands/", views.BandView.as_view(), name="bands"),
    path("molecules/", views.MoleculeView.as_view(), name="molecules"),
    path("data/", views.DataView.as_view(), name="data"),
    path(
        "generate-script/",
        DownloadScriptGeneratorView.as_view(),
        name="generate-script",
    ),
]
