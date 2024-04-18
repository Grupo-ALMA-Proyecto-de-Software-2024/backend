from typing import Any, List
from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest


class AlmaAdminSite(admin.AdminSite):
    site_header = "ALMA Administration"
    site_title = "ALMA Administration"
    index_title = "ALMA Administration"

    def get_app_list(self, request: WSGIRequest) -> List[Any]:
        apps = super().get_app_list(request)
        print(f"apps: {apps}")
        return apps
