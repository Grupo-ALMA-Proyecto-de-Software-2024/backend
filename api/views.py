from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .models import CarouselImage
from .serializers import CarouselImageSerializer


class HelloWorldView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        return Response({"message": "Hello, World!"})


class CarouselImageView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request):
        carousel_images = CarouselImage.objects.all()
        serializer = CarouselImageSerializer(carousel_images, many=True)
        return Response(serializer.data)

    @classmethod
    def get_serializer_class(cls):
        return CarouselImageSerializer
