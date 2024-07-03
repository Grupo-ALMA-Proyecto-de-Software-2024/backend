# content_management/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from django.conf import settings

from .service import generate_download_script_service


class DownloadScriptGeneratorView(APIView):
    @extend_schema(
        tags=["Download Script"],
        request={
            "application/json": {
                "example": {
                    "links": ["https://example.com/file1", "https://example.com/file2"],
                }
            }
        },
        responses={
            200: {"example": {"script_url": "/media/scripts/download_data.sh"}},
            400: {"description": "Invalid input data."},
        },
    )
    def post(self, request):
        try:
            links = request.data.get("links", [])
            if not links:
                return Response(
                    {"error": "Links are required."}, status=status.HTTP_400_BAD_REQUEST
                )

            script_url = generate_download_script_service(
                links=links, total_size_msg="Total size: <X> MB"
            )
            return Response({"script_url": f"{settings.MEDIA_URL}{script_url}"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
