from django.test import TestCase
from ..models import Region, Disk, Band, Molecule, Data
from ..serializers.full_context_serializers import (
    FullContextDataSerializer,
    FullContextMoleculeSerializer,
    FullContextBandSerializer,
    FullContextDiskSerializer,
    FullContextRegionSerializer,
)


class FullContextSerializerTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Region1")
        self.disk = Disk.objects.create(name="Disk1", region=self.region)
        self.band = Band.objects.create(name="Band1", disk=self.disk)
        self.molecule = Molecule.objects.create(name="Molecule1", band=self.band)
        self.data = Data.objects.create(
            name="Data1", molecule=self.molecule, file="file1", is_viewable=True
        )

    def test_data_serializer(self):
        serializer = FullContextDataSerializer(instance=self.data)
        expected_data = {
            "name": "Data1",
            "creation_date": self.data.creation_date.isoformat().replace(
                "+00:00", "Z"
            ),  # ensuring the format matches
            "molecule_name": "Molecule1",
            "band_name": "Band1",
            "disk_name": "Disk1",
            "region_name": "Region1",
            "file": self.data.file.url,  # Accessing the full URL if MEDIA_URL is set
            "is_viewable": True,
        }
        self.assertEqual(serializer.data, expected_data)

    def test_molecule_serializer(self):
        serializer = FullContextMoleculeSerializer(instance=self.molecule)
        expected_data = {
            "name": "Molecule1",
            "band_name": "Band1",
            "disk_name": "Disk1",
            "region_name": "Region1",
            "data": [
                {
                    "name": "Data1",
                    "creation_date": self.data.creation_date.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    "file": self.data.file.url,
                    "is_viewable": True,
                }
            ],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_band_serializer(self):
        serializer = FullContextBandSerializer(instance=self.band)
        expected_data = {
            "name": "Band1",
            "disk_name": "Disk1",
            "region_name": "Region1",
            "molecules": [
                {
                    "name": "Molecule1",
                    "data": [
                        {
                            "name": "Data1",
                            "creation_date": self.data.creation_date.isoformat().replace(
                                "+00:00", "Z"
                            ),
                            "file": self.data.file.url,
                            "is_viewable": True,
                        }
                    ],
                }
            ],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_disk_serializer(self):
        serializer = FullContextDiskSerializer(instance=self.disk)
        expected_data = {
            "name": "Disk1",
            "region_name": "Region1",
            "bands": [
                {
                    "name": "Band1",
                    "molecules": [
                        {
                            "name": "Molecule1",
                            "data": [
                                {
                                    "name": "Data1",
                                    "creation_date": self.data.creation_date.isoformat().replace(
                                        "+00:00", "Z"
                                    ),
                                    "file": self.data.file.url,
                                    "is_viewable": True,
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_region_serializer(self):
        serializer = FullContextRegionSerializer(instance=self.region)
        expected_data = {
            "name": "Region1",
            "disks": [
                {
                    "name": "Disk1",
                    "bands": [
                        {
                            "name": "Band1",
                            "molecules": [
                                {
                                    "name": "Molecule1",
                                    "data": [
                                        {
                                            "name": "Data1",
                                            "creation_date": self.data.creation_date.isoformat().replace(
                                                "+00:00", "Z"
                                            ),
                                            "file": self.data.file.url,
                                            "is_viewable": True,
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        self.assertEqual(serializer.data, expected_data)
