from typing import Any, List
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest


def sort_models_in_app_list(
    apps: List[Any],
    app_name: str,
    model_order: List[str],
) -> List[Any]:
    """
    Sorts the models in the app list by the order of the model_order list.
    If the app is not found, the app list is returned as is.
    Args:
        apps: The app list, as returned by the get_app_list method (django)
        app_name: The name of the app to sort.
        model_order: The order of the models wanted in the app.
    """
    app = next((app for app in apps if app["name"] == app_name), None)
    if app:
        app["models"] = sorted(app["models"], key=lambda x: model_order.index(x["object_name"]))
        print(app["models"])
    return apps


order_of_api_models = [
    "Region",
    "Disk",
    "Band",
    "Molecule",
    "CarouselImage",
]


class AlmaAdminSite(admin.AdminSite):
    site_header = "ALMA Administration"
    site_title = "ALMA Administration"
    index_title = "ALMA Administration"

    def get_app_list(self, request: WSGIRequest) -> List[Any]:
        apps = super().get_app_list(request)
        apps = sort_models_in_app_list(apps, "API", order_of_api_models)
        return apps
