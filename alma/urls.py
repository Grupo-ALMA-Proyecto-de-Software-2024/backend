from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from alma.admin import admin_site


def health_check(request):
    return HttpResponse("Service is healthy", status=200)


urlpatterns = [
    path("", health_check, name="health-check"),
    path("admin/", admin_site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("content-management/", include("content_management.urls")),
    # API schema and documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui-api",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc-api",
    ),
    # Optional: shortcut to Swagger
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui-docs",
    ),
]

# Serve static and media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
