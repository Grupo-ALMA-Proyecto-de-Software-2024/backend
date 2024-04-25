from rest_framework import serializers
from .. import models


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarouselImage
        fields = ["image", "title", "description", "creation_date"]


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Data
        fields = ["name", "creation_date", "file", "is_viewable"]


class MoleculeSerializer(serializers.ModelSerializer):
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.Molecule
        fields = ["name", "data"]


class BandSerializer(serializers.ModelSerializer):
    molecules = MoleculeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Band
        fields = ["name", "molecules"]


class DiskSerializer(serializers.ModelSerializer):
    bands = BandSerializer(many=True, read_only=True)

    class Meta:
        model = models.Disk
        fields = ["name", "bands"]


class RegionSerializer(serializers.ModelSerializer):
    disks = DiskSerializer(many=True, read_only=True)

    class Meta:
        model = models.Region
        fields = ["name", "disks"]
