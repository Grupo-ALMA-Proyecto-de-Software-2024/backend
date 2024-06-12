from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from . import models, serializers


class CarouselImageView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request: Request):
        carousel_images = models.CarouselImage.objects.all()
        serializer = serializers.CarouselImageSerializer(carousel_images, many=True)
        return Response({"carousel_images": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.CarouselImageSerializer


class PublicationView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request: Request):
        publications = models.Publication.objects.all()
        serializer = serializers.PublicationSerializer(publications, many=True)
        return Response({"publications": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.PublicationSerializer


class PressNewsView(APIView):
    @extend_schema(tags=["API"])
    def get(self, request: Request):
        press_news = models.PressNews.objects.all()
        serializer = serializers.PressNewsSerializer(press_news, many=True)
        return Response({"press_news": serializer.data})

    @classmethod
    def get_serializer_class(cls):
        return serializers.PressNewsSerializer
