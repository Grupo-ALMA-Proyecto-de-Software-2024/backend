from PIL import Image
from pathlib import Path

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import CarouselImage


class CarouselImageViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        image = Image.new("RGB", (100, 100))
        self.image_path = Path("test_image.jpg")
        image.save(self.image_path)

        self.uploaded_image = SimpleUploadedFile(
            self.image_path.name,
            self.image_path.read_bytes(),
            content_type="image/jpeg",
        )

        self.carousel_image = CarouselImage.objects.create(
            image=self.uploaded_image,
            title="Test Image",
            description="Test Description",
        )

    def tearDown(self):
        self.image_path.unlink()

    def test_carousel_image_list(self):
        response = self.client.get(reverse("carousel"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Image")
        self.assertEqual(response.data[0]["description"], "Test Description")
        self.assertEqual(response.data[0]["image"], self.carousel_image.image.url)
