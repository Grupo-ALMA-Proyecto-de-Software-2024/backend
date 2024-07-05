from django.test import TestCase
from ..models import Region, Disk, Band, Molecule, Data
from ..serializers import (
    DataSerializer,
    MoleculeSerializer,
    BandSerializer,
    DiskSerializer,
    RegionSerializer,
)


class SerializerTest(TestCase):
    def setUp(self):
        self.region = Region.objects.create(name="Region1")
        self.disk = Disk.objects.create(name="Disk1")
        self.disk.regions.add(self.region)
        self.band = Band.objects.create(name="Band1")
        self.band.disks.add(self.disk)
        self.molecule = Molecule.objects.create(name="Molecule1")
        self.molecule.bands.add(self.band)
        self.data = Data.objects.create(
            name="Data1",
            molecule=self.molecule,
            band=self.band,
            disk=self.disk,
            region=self.region,
            filepath="file1",
            image_link="http://example.com/image.png",  # Changed to use `image_link`
        )

    def test_data_serializer(self):
        serializer = DataSerializer(instance=self.data)
        expected_data = {
            "name": "Data1",
            "region": "Region1",
            "disk": "Disk1",
            "band": "Band1",
            "molecule": "Molecule1",
            "filepath": self.data.filepath,
            "image_link": "http://example.com/image.png",  # Updated to check `image_link`
        }
        self.assertEqual(serializer.data, expected_data)

    def test_molecule_serializer(self):
        serializer = MoleculeSerializer(instance=self.molecule)
        expected_data = {
            "name": "Molecule1",
            "creation_date": self.molecule.creation_date.isoformat().replace(
                "+00:00", "Z"
            ),
            "data": [
                {
                    "name": "Data1",
                    "region": "Region1",
                    "disk": "Disk1",
                    "band": "Band1",
                    "molecule": "Molecule1",
                    "filepath": self.data.filepath,
                    "image_link": "http://example.com/image.png",  # Updated to include `image_link`
                }
            ],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_band_serializer(self):
        serializer = BandSerializer(instance=self.band)
        expected_data = {
            "name": "Band1",
            "creation_date": self.band.creation_date.isoformat().replace("+00:00", "Z"),
            "molecules": [
                {
                    "name": "Molecule1",
                    "creation_date": self.molecule.creation_date.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    "data": [
                        {
                            "name": "Data1",
                            "region": "Region1",
                            "disk": "Disk1",
                            "band": "Band1",
                            "molecule": "Molecule1",
                            "filepath": self.data.filepath,
                            "image_link": "http://example.com/image.png",  # Updated to use `image_link`
                        }
                    ],
                }
            ],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_disk_serializer(self):
        serializer = DiskSerializer(instance=self.disk)
        expected_data = {
            "name": "Disk1",
            "creation_date": self.disk.creation_date.isoformat().replace("+00:00", "Z"),
            "bands": [
                {
                    "name": "Band1",
                    "creation_date": self.band.creation_date.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    "molecules": [
                        {
                            "name": "Molecule1",
                            "creation_date": self.molecule.creation_date.isoformat().replace(
                                "+00:00", "Z"
                            ),
                            "data": [
                                {
                                    "name": "Data1",
                                    "region": "Region1",
                                    "disk": "Disk1",
                                    "band": "Band1",
                                    "molecule": "Molecule1",
                                    "filepath": self.data.filepath,
                                    "image_link": "http://example.com/image.png",  # Updated to use `image_link`
                                }
                            ],
                        }
                    ],
                }
            ],
        }
        self.assertEqual(serializer.data, expected_data)

    def test_region_serializer(self):
        serializer = RegionSerializer(instance=self.region)
        expected_data = {
            "name": "Region1",
            "creation_date": self.region.creation_date.isoformat().replace(
                "+00:00", "Z"
            ),
            "disks": [
                {
                    "name": "Disk1",
                    "creation_date": self.disk.creation_date.isoformat().replace(
                        "+00:00", "Z"
                    ),
                    "bands": [
                        {
                            "name": "Band1",
                            "creation_date": self.band.creation_date.isoformat().replace(
                                "+00:00", "Z"
                            ),
                            "molecules": [
                                {
                                    "name": "Molecule1",
                                    "creation_date": self.molecule.creation_date.isoformat().replace(
                                        "+00:00", "Z"
                                    ),
                                    "data": [
                                        {
                                            "name": "Data1",
                                            "region": "Region1",
                                            "disk": "Disk1",
                                            "band": "Band1",
                                            "molecule": "Molecule1",
                                            "filepath": self.data.filepath,
                                            "image_link": "http://example.com/image.png",  # Updated to use `image_link`
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
