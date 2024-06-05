from rest_framework import serializers
from . import models


class DataSerializer(serializers.ModelSerializer):
    region = serializers.SerializerMethodField()
    disk = serializers.SerializerMethodField()
    band = serializers.SerializerMethodField()
    molecule = serializers.SerializerMethodField()

    class Meta:
        model = models.Data
        fields = ["region", "disk", "band", "molecule", "file", "is_viewable"]

    def get_region(self, obj):
        return obj.region.name

    def get_disk(self, obj):
        return obj.disk.name

    def get_band(self, obj):
        return obj.band.name

    def get_molecule(self, obj):
        return obj.molecule.name


class MoleculeSerializer(serializers.ModelSerializer):
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.Molecule
        fields = "__all__"


class BandSerializer(serializers.ModelSerializer):
    molecules = MoleculeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Band
        fields = "__all__"


class DiskSerializer(serializers.ModelSerializer):
    bands = BandSerializer(many=True, read_only=True)

    class Meta:
        model = models.Disk
        fields = "__all__"


class RegionSerializer(serializers.ModelSerializer):
    disks = DiskSerializer(many=True, read_only=True)

    class Meta:
        model = models.Region
        fields = "__all__"
