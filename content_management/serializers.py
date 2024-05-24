from rest_framework import serializers

from . import models


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarouselImage
        fields = ["image", "title", "description", "creation_date"]