from rest_framework import serializers
from .. import models
from .compact_serializers import (
    BandSerializer,
    DiskSerializer,
    MoleculeSerializer,
    DataSerializer,
)


class FullContextDataSerializer(serializers.ModelSerializer):
    molecule_name = serializers.ReadOnlyField(source="molecule.name")
    band_name = serializers.ReadOnlyField(source="molecule.band.name")
    disk_name = serializers.ReadOnlyField(source="molecule.band.disk.name")
    region_name = serializers.ReadOnlyField(source="molecule.band.disk.region.name")

    class Meta:
        model = models.Data
        fields = [
            "name",
            "creation_date",
            "molecule_name",
            "band_name",
            "disk_name",
            "region_name",
            "file",
            "is_viewable",
        ]


class FullContextMoleculeSerializer(serializers.ModelSerializer):
    band_name = serializers.ReadOnlyField(source="band.name")
    disk_name = serializers.ReadOnlyField(source="band.disk.name")
    region_name = serializers.ReadOnlyField(source="band.disk.region.name")
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = models.Molecule
        fields = ["name", "band_name", "disk_name", "region_name", "data"]


class FullContextBandSerializer(serializers.ModelSerializer):
    disk_name = serializers.ReadOnlyField(source="disk.name")
    region_name = serializers.ReadOnlyField(source="disk.region.name")
    molecules = MoleculeSerializer(many=True, read_only=True)

    class Meta:
        model = models.Band
        fields = ["name", "disk_name", "region_name", "molecules"]


class FullContextDiskSerializer(serializers.ModelSerializer):
    region_name = serializers.ReadOnlyField(source="region.name")
    bands = BandSerializer(many=True, read_only=True)

    class Meta:
        model = models.Disk
        fields = ["name", "region_name", "bands"]


class FullContextRegionSerializer(serializers.ModelSerializer):
    disks = DiskSerializer(many=True, read_only=True)

    class Meta:
        model = models.Region
        fields = ["name", "disks"]
