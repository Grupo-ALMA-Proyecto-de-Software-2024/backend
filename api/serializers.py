from rest_framework import serializers

from . import models


class HelloSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=100)


class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarouselImage
        fields = ["image", "title", "description", "creation_date"]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Region
        fields = ["name"]


class DiskSerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()

    class Meta:
        model = models.Disk
        fields = ["name", "region"]


class BandSerializer(serializers.ModelSerializer):
    disk = serializers.StringRelatedField()
    region = serializers.StringRelatedField()

    class Meta:
        model = models.Band
        fields = ["name", "disk", "region"]

    def get_disk(self, obj):
        return obj.disk.name

    def get_region(self, obj):
        return obj.disk.region.name


class MoleculeSerializer(serializers.ModelSerializer):
    band = serializers.StringRelatedField()
    disk = serializers.StringRelatedField()
    region = serializers.StringRelatedField()

    class Meta:
        model = models.Molecule
        fields = ["name", "band", "disk", "region"]

    def get_band(self, obj):
        return obj.band.name

    def get_disk(self, obj):
        return obj.band.disk.name

    def get_region(self, obj):
        return obj.band.disk.region.name


class DataSerializer(serializers.ModelSerializer):
    molecule = serializers.SerializerMethodField()
    band = serializers.SerializerMethodField()
    disk = serializers.SerializerMethodField()
    region = serializers.SerializerMethodField()

    class Meta:
        model = models.Data
        fields = [
            "name",
            "creation_date",
            "molecule",
            "band",
            "disk",
            "region",
            "file",
            "is_viewable",
        ]

    def get_molecule(self, obj):
        return obj.molecule.name

    def get_band(self, obj):
        return obj.molecule.band.name

    def get_disk(self, obj):
        return obj.molecule.band.disk.name

    def get_region(self, obj):
        return obj.molecule.band.disk.region.name
