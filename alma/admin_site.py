from typing import Any, List, Dict
from django.contrib import admin


def find_app(apps: Dict[str, Any], app_name: str) -> Any:
    return next((app for app in apps.values() if app["name"] == app_name), None)


def sort_apps(apps: Dict[str, Any], app_order: List[str]) -> Dict[str, Any]:
    """
    Sort the apps in the order specified by app_order.
    Args:
        apps: A dictionary of apps to sort, comes from self._build_app_dict (django)
        app_order: A list of app names in the order they should be sorted.
    Returns:
        The same dictionary of apps, but sorted.
    """
    try:
        sorted_apps = sorted(
            apps.values(),
            key=lambda app: app_order.index(app["name"]),
        )
    except ValueError as e:
        if "not in list" in str(e):
            print(f"{e}: {app_order}")
            raise e
        raise e
    return sorted_apps


def sort_models_within_app(
    apps: Dict[str, Any],
    app_name: str,
    model_order: List[str],
) -> Dict[str, Any]:
    """
    Sort the models within an app in the order specified by model_order.
    Args:
        app: A dictionary of an app to sort, comes from self._build_app_dict (django)
        app_name: The name of the app to sort.
        model_order: A list of model names in the order they should be sorted.
    Returns:
        The same dictionary of an app, but with models sorted.
    """
    app = find_app(apps=apps, app_name=app_name)
    try:
        sorted_models = sorted(
            app["models"],
            key=lambda model: model_order.index(model["name"]),
        )
    except ValueError as e:
        if "not in list" in str(e):
            print(f"{e}: {model_order}")
            raise e
        raise e
    return sorted_models


MODELS_TEMPLATE = [
    {
        "app_backend_name": "Api",
        "name_to_display": "Recursos",
        "models": [
            "Regions",
            "Disks",
            "Bands",
            "Molecules",
            "Carousel images",
        ],
    },
    {
        "app_backend_name": "Authentication and Authorization",
        "name_to_display": "Usuarios",
        "models": [
            "User",
        ],
    },
]


def update_apps_organization(apps: Dict[str, Any], template: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Update the organization of the apps and models in the admin site.
    Args:
        apps: A dictionary of apps to sort, comes from self._build_app_dict (django)
        template: A list of dictionaries with the organization of the apps and models.
    Returns:
        The same dictionary of apps, but with the updated organization.
    """
    for app in template:
        app_name = app["app_backend_name"]
        models = app["models"]
        sort_models_within_app(
            apps=apps,
            app_name=app_name,
            model_order=models,
        )
    return apps


class AlmaAdminSite(admin.AdminSite):
    site_header = "ALMA Administration"
    site_title = "ALMA Administration"
    index_title = "ALMA Administration"

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps alphabetically.
        app_list = sort_apps(
            apps=app_dict,
            app_order=[
                "Authentication and Authorization",
                "Api",
            ],
        )

        sort_models_within_app(
            apps=app_dict,
            app_name="Api",
            model_order=[
                "Regions",
                "Disks",
                "Bands",
                "Molecules",
                "Carousel images",
            ],
        )

        return app_list
