from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase

from ..models import Region, Disk, Band, Molecule, Data


class ViewNoQueryParamsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create test data
        self.region = Region.objects.create(name="Region1")
        self.disk = Disk.objects.create(name="Disk1", region=self.region)
        self.band = Band.objects.create(name="Band1", disk=self.disk)
        self.molecule = Molecule.objects.create(name="Molecule1", band=self.band)
        self.data = Data.objects.create(
            name="Data1", molecule=self.molecule, file="file1", is_viewable=True
        )

    def test_region_view(self):
        url = reverse("regions")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(
            "regions", response.data
        )  # Check if 'regions' is part of the response
        self.assertEqual(len(response.data["regions"]), 1)  # Assuming 1 region
        self.assertEqual(response.data["regions"][0]["name"], "Region1")

    def test_disk_view(self):
        url = reverse("disks")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("disks", response.data)
        self.assertEqual(len(response.data["disks"]), 1)
        self.assertEqual(response.data["disks"][0]["name"], "Disk1")

    def test_band_view(self):
        url = reverse("bands")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bands", response.data)
        self.assertEqual(len(response.data["bands"]), 1)
        self.assertEqual(response.data["bands"][0]["name"], "Band1")

    def test_molecule_view(self):
        url = reverse("molecules")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("molecules", response.data)
        self.assertEqual(len(response.data["molecules"]), 1)
        self.assertEqual(response.data["molecules"][0]["name"], "Molecule1")

    def test_data_view(self):
        url = reverse("data")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "Data1")


class ViewTestWithQueryParams(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.region1 = Region.objects.create(name="Region1")
        self.region2 = Region.objects.create(name="Region2")
        self.disk1 = Disk.objects.create(name="Disk1", region=self.region1)
        self.disk2 = Disk.objects.create(name="Disk2", region=self.region2)
        self.band1 = Band.objects.create(name="Band1", disk=self.disk1)
        self.band2 = Band.objects.create(name="Band2", disk=self.disk2)
        self.molecule1 = Molecule.objects.create(name="Molecule1", band=self.band1)
        self.molecule2 = Molecule.objects.create(name="Molecule2", band=self.band2)
        self.data1 = Data.objects.create(
            name="Data1", molecule=self.molecule1, file="file1", is_viewable=True
        )
        self.data2 = Data.objects.create(
            name="Data2", molecule=self.molecule2, file="file2", is_viewable=True
        )

    def test_region_view_with_filter(self):
        url = reverse("regions") + "?region=Region1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("regions", response.data)
        self.assertEqual(len(response.data["regions"]), 1)
        self.assertEqual(response.data["regions"][0]["name"], "Region1")

    def test_disk_view_with_filter(self):
        url = reverse("disks") + "?disk=Disk1&region=Region1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("disks", response.data)
        self.assertEqual(len(response.data["disks"]), 1)
        self.assertEqual(response.data["disks"][0]["name"], "Disk1")

    def test_band_view_with_filter(self):
        url = reverse("bands") + "?band=Band1&disk=Disk1&region=Region1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bands", response.data)
        self.assertEqual(len(response.data["bands"]), 1)
        self.assertEqual(response.data["bands"][0]["name"], "Band1")

    def test_molecule_view_with_filter(self):
        url = (
            reverse("molecules")
            + "?molecule=Molecule1&band=Band1&disk=Disk1&region=Region1"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("molecules", response.data)
        self.assertEqual(len(response.data["molecules"]), 1)
        self.assertEqual(response.data["molecules"][0]["name"], "Molecule1")

    def test_data_view_with_filter(self):
        url = (
            reverse("data")
            + "?data=Data1&molecule=Molecule1&band=Band1&disk=Disk1&region=Region1"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "Data1")
