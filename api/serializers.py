from rest_framework import serializers
from . import models


class DataSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    disk = serializers.SerializerMethodField()
    band = serializers.SerializerMethodField()
    molecule = serializers.SerializerMethodField()

    class Meta:
        model = models.Data
        fields = [
            "name",
            "region",
            "disk",
            "band",
            "molecule",
            "filepath",
            "image_link",
            "size_in_mb",
        ]

    def get_region(self, obj):
        return obj.region.name

    def get_disk(self, obj):
        return obj.disk.name

    def get_band(self, obj):
        return obj.band.name

    def get_molecule(self, obj):
        return obj.molecule.name


class MoleculeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Molecule
        fields = ["name", "creation_date"]


class BandSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Band
        fields = ["name", "creation_date"]


class DiskSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Disk
        fields = ["name", "creation_date", "features"]


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Region
        fields = ["name", "creation_date", "description"]
