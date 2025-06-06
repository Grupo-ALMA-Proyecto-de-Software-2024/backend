"""
URL configuration for alma project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from alma.admin import admin_site


def health_check(request):
    return HttpResponse("Service is healthy", status=200)


# All application-specific URLs are grouped here to be prefixed.
backend_urlpatterns = [
    path("admin/", admin_site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("content-management/", include("content_management.urls")),
    # The schema and docs are now part of the backend prefix.
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="backend:schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="backend:schema"),
        name="redoc",
    ),
]

urlpatterns = [
    path("", health_check, name="health-check"),
    # All backend URLs are now served under the /backend/ prefix.
    path("backend/", include((backend_urlpatterns, "backend"), namespace="backend")),
]

# In development, Django serves static and media files.
# In production, Nginx is configured to handle these.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # In production, we still need to define the static and media URL patterns,
    # even if Nginx is serving the files, so that Django's template tags
    # like {% static 'path/to/file' %} can resolve the URLs correctly.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
