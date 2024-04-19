from typing import Any, List, Dict
from django.contrib import admin


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
            "Users",
        ],
    },
]


def find_app(apps: Dict[str, Any], app_name: str) -> Any:
    return next((app for app in apps.values() if app["name"] == app_name), None)


def update_apps_layout(
    apps: Dict[str, Any],
    template: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Update the layout of the apps based on the template.
    Args:
        apps: A dictionary of apps to sort, comes from self._build_app_dict (django)
        template: A list of dictionaries with the following structure:
            {
                "app_backend_name": "<app_name>",
                "name_to_display": "<name_to_display>",
                "models": ["<list of models in the order to display>"],
            }
    Returns:
        The same dictionary of apps, but with the layout updated. The order of the apps and models
        will be the same as the template.
    """
    for app in template:
        app_backend_name = app["app_backend_name"]
        app_name_to_display = app["name_to_display"]
        models = app["models"]

        app_to_update = find_app(apps, app_backend_name)
        if app_to_update:
            app_to_update["name"] = app_name_to_display
            app_to_update["models"].sort(key=lambda model: models.index(model["name"]))

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

        app_dict = update_apps_layout(app_dict, MODELS_TEMPLATE)

        return list(app_dict.values())
