from rest_framework import serializers

from .models import CarouselImage


class HelloSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ["image", "title", "description", "creation_date"]
