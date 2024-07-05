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
            image_link="http://example.com/image.png",
            size_in_mb=1.0,
        )

    def test_region_view(self):
        url = reverse("regions")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("regions", response.data)
        self.assertEqual(len(response.data["regions"]), 1)
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
        self.disk1 = Disk.objects.create(name="Disk1")
        self.disk1.regions.add(self.region1)
        self.disk2 = Disk.objects.create(name="Disk2")
        self.disk2.regions.add(self.region2)
        self.band1 = Band.objects.create(name="Band1")
        self.band1.disks.add(self.disk1)
        self.band2 = Band.objects.create(name="Band2")
        self.band2.disks.add(self.disk2)
        self.molecule1 = Molecule.objects.create(name="Molecule1")
        self.molecule1.bands.add(self.band1)
        self.molecule2 = Molecule.objects.create(name="Molecule2")
        self.molecule2.bands.add(self.band2)
        self.data1 = Data.objects.create(
            name="Data1",
            molecule=self.molecule1,
            band=self.band1,
            disk=self.disk1,
            region=self.region1,
            filepath="file1",
            image_link="http://example.com/image.png",
            size_in_mb=1.0,
        )
        self.data2 = Data.objects.create(
            name="Data2",
            molecule=self.molecule2,
            band=self.band2,
            disk=self.disk2,
            region=self.region2,
            filepath="file2",
            image_link="http://example.com/image.png",
            size_in_mb=2.0,
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
        self.assertEqual(response.data["data"][0]["size_in_mb"], 1.0)
        self.assertEqual(
            response.data["data"][0]["image_link"], "http://example.com/image.png"
        )
        self.assertEqual(response.data["data"][0]["filepath"], "file1")


class ViewTestWithMultipleFilters(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.region1 = Region.objects.create(name="Region1")
        self.region2 = Region.objects.create(name="Region2")
        self.disk1 = Disk.objects.create(name="Disk1")
        self.disk1.regions.add(self.region1)
        self.disk2 = Disk.objects.create(name="Disk2")
        self.disk2.regions.add(self.region2)
        self.band1 = Band.objects.create(name="Band1")
        self.band1.disks.add(self.disk1)
        self.band2 = Band.objects.create(name="Band2")
        self.band2.disks.add(self.disk2)
        self.molecule1 = Molecule.objects.create(name="Molecule1")
        self.molecule1.bands.add(self.band1)
        self.molecule2 = Molecule.objects.create(name="Molecule2")
        self.molecule2.bands.add(self.band2)
        self.data1 = Data.objects.create(
            name="Data1",
            molecule=self.molecule1,
            band=self.band1,
            disk=self.disk1,
            region=self.region1,
            filepath="file1",
            image_link="http://example.com/image.png",
            size_in_mb=1.0,
        )
        self.data2 = Data.objects.create(
            name="Data2",
            molecule=self.molecule2,
            band=self.band2,
            disk=self.disk2,
            region=self.region2,
            filepath="file2",
            image_link="http://example.com/image.png",
            size_in_mb=2.0,
        )

    def test_region_view_with_multiple_filters(self):
        url = reverse("regions") + "?region=Region1&region=Region2"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("regions", response.data)
        self.assertEqual(len(response.data["regions"]), 2)
        self.assertEqual(response.data["regions"][0]["name"], "Region1")
        self.assertEqual(response.data["regions"][1]["name"], "Region2")

    def test_disk_view_with_multiple_filters(self):
        url = reverse("disks") + "?disk=Disk1&disk=Disk2&region=Region1&region=Region2"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("disks", response.data)
        self.assertEqual(len(response.data["disks"]), 2)
        self.assertEqual(response.data["disks"][0]["name"], "Disk1")
        self.assertEqual(response.data["disks"][1]["name"], "Disk2")

    def test_band_view_with_multiple_filters(self):
        url = (
            reverse("bands")
            + "?band=Band1&band=Band2&disk=Disk1&disk=Disk2&region=Region1&region=Region2"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bands", response.data)
        self.assertEqual(len(response.data["bands"]), 2)
        self.assertEqual(response.data["bands"][0]["name"], "Band1")
        self.assertEqual(response.data["bands"][1]["name"], "Band2")

    def test_molecule_view_with_multiple_filters(self):
        url = (
            reverse("molecules")
            + "?molecule=Molecule1&molecule=Molecule2&band=Band1&band=Band2"
            + "&disk=Disk1&disk=Disk2&region=Region1&region=Region2"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("molecules", response.data)
        self.assertEqual(len(response.data["molecules"]), 2)
        self.assertEqual(response.data["molecules"][0]["name"], "Molecule1")
        self.assertEqual(response.data["molecules"][1]["name"], "Molecule2")

    def test_data_view_with_multiple_filters(self):
        url = (
            reverse("data")
            + "?data=Data1&data=Data2&molecule=Molecule1&molecule=Molecule2"
            + "&band=Band1&band=Band2&disk=Disk1&disk=Disk2&region=Region1&region=Region2"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(len(response.data["data"]), 2)
        self.assertEqual(response.data["data"][0]["name"], "Data1")
        self.assertEqual(response.data["data"][1]["name"], "Data2")
        self.assertEqual(response.data["data"][0]["size_in_mb"], 1.0)
        self.assertEqual(response.data["data"][1]["size_in_mb"], 2.0)

    def test_region_view_with_filter_and_a_non_existent_region(self):
        url = reverse("regions") + "?region=Region1&region=Region3"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("regions", response.data)
        self.assertEqual(len(response.data["regions"]), 1)
        self.assertEqual(response.data["regions"][0]["name"], "Region1")

    def test_disk_view_with_filter_and_a_non_existent_disk(self):
        url = reverse("disks") + "?disk=Disk1&disk=Disk3&region=Region1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("disks", response.data)
        self.assertEqual(len(response.data["disks"]), 1)
        self.assertEqual(response.data["disks"][0]["name"], "Disk1")

    def test_band_view_with_filter_and_a_non_existent_band(self):
        url = reverse("bands") + "?band=Band1&band=Band3&disk=Disk1&region=Region1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bands", response.data)
        self.assertEqual(len(response.data["bands"]), 1)
        self.assertEqual(response.data["bands"][0]["name"], "Band1")

    def test_molecule_view_with_filter_and_a_non_existent_molecule(self):
        url = (
            reverse("molecules")
            + "?molecule=Molecule1&molecule=Molecule3&band=Band1&disk=Disk1&region=Region1"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("molecules", response.data)
        self.assertEqual(len(response.data["molecules"]), 1)
        self.assertEqual(response.data["molecules"][0]["name"], "Molecule1")

    def test_data_view_with_filter_and_a_non_existent_data(self):
        url = (
            reverse("data")
            + "?data=Data1&data=Data3&molecule=Molecule1&band=Band1&disk=Disk1&region=Region1"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["name"], "Data1")
        self.assertEqual(response.data["data"][0]["size_in_mb"], 1.0)


class ViewTestWithNoResults(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.region1 = Region.objects.create(name="Region1")
        self.region2 = Region.objects.create(name="Region2")
        self.disk1 = Disk.objects.create(name="Disk1")
        self.disk1.regions.add(self.region1)
        self.disk2 = Disk.objects.create(name="Disk2")
        self.disk2.regions.add(self.region2)
        self.band1 = Band.objects.create(name="Band1")
        self.band1.disks.add(self.disk1)
        self.band2 = Band.objects.create(name="Band2")
        self.band2.disks.add(self.disk2)
        self.molecule1 = Molecule.objects.create(name="Molecule1")
        self.molecule1.bands.add(self.band1)
        self.molecule2 = Molecule.objects.create(name="Molecule2")
        self.molecule2.bands.add(self.band2)
        self.data1 = Data.objects.create(
            name="Data1",
            molecule=self.molecule1,
            band=self.band1,
            disk=self.disk1,
            region=self.region1,
            filepath="file1",
            image_link="http://example.com/image.png",
            size_in_mb=1.0,
        )
        self.data2 = Data.objects.create(
            name="Data2",
            molecule=self.molecule2,
            band=self.band2,
            disk=self.disk2,
            region=self.region2,
            filepath="file2",
            image_link="http://example.com/image.png",
            size_in_mb=2.0,
        )

    def test_region_view_no_results(self):
        url = reverse("regions") + "?region=Region3"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("regions", response.data)
        self.assertEqual(len(response.data["regions"]), 0)

    def test_disk_view_no_results(self):
        url = reverse("disks") + "?disk=Disk3&region=Region3"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("disks", response.data)
        self.assertEqual(len(response.data["disks"]), 0)

    def test_band_view_no_results(self):
        url = reverse("bands") + "?band=Band3&disk=Disk3&region=Region3"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("bands", response.data)
        self.assertEqual(len(response.data["bands"]), 0)

    def test_molecule_view_no_results(self):
        url = (
            reverse("molecules")
            + "?molecule=Molecule3&band=Band3&disk=Disk3&region=Region3"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("molecules", response.data)
        self.assertEqual(len(response.data["molecules"]), 0)

    def test_data_view_no_results(self):
        url = (
            reverse("data")
            + "?data=Data3&molecule=Molecule3&band=Band3&disk=Disk3&region=Region3"
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("data", response.data)
        self.assertEqual(len(response.data["data"]), 0)
