from rest_framework import serializers

from . import models


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarouselImage
        fields = ["image", "title", "description", "creation_date"]


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Publication
        fields = "__all__"


class PressNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PressNews
        fields = ["content", "creation_date"]
