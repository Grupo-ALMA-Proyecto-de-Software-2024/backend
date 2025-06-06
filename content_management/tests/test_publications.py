from pathlib import Path

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.test import APIClient
from PIL import Image

from ..models import Publication


class PublicationViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        image = Image.new("RGB", (100, 100))
        self.image_path = Path("test_publication_image.jpg")
        image.save(self.image_path)

        self.uploaded_image = SimpleUploadedFile(
            self.image_path.name,
            self.image_path.read_bytes(),
            content_type="image/jpeg",
        )

        self.publication = Publication.objects.create(
            title="Test Publication",
            authors="Author1, Author2",
            full_authors="Author1, Author2",
            journal_info="Journal of Testing",
            summary="This is a test summary.",
            image=self.uploaded_image,
            pdf_link="http://example.com/test.pdf",
            bibtex_link="http://example.com/test.bib",
            data_link="http://example.com/test.data",
            sao_nasa_link="http://example.com/test.sao",
        )

    def tearDown(self):
        self.image_path.unlink()

    def test_publication_list(self):
        response = self.client.get(reverse("backend:publications"))
        response_data = response.data["publications"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["title"], "Test Publication")
        self.assertEqual(response_data[0]["authors"], "Author1, Author2")
        self.assertEqual(response_data[0]["full_authors"], "Author1, Author2")
        self.assertEqual(response_data[0]["journal_info"], "Journal of Testing")
        self.assertEqual(response_data[0]["summary"], "This is a test summary.")
        self.assertEqual(response_data[0]["image"], self.publication.image.url)
        self.assertEqual(response_data[0]["pdf_link"], "http://example.com/test.pdf")
        self.assertEqual(response_data[0]["bibtex_link"], "http://example.com/test.bib")
        self.assertEqual(response_data[0]["data_link"], "http://example.com/test.data")
        self.assertEqual(
            response_data[0]["sao_nasa_link"], "http://example.com/test.sao"
        )

    def test_publication_fields(self):
        publication = Publication.objects.get(id=self.publication.id)
        self.assertEqual(publication.title, "Test Publication")
        self.assertEqual(publication.authors, "Author1, Author2")
        self.assertEqual(publication.full_authors, "Author1, Author2")
        self.assertEqual(publication.journal_info, "Journal of Testing")
        self.assertEqual(publication.summary, "This is a test summary.")
        self.assertEqual(publication.image.url, self.publication.image.url)
        self.assertEqual(publication.pdf_link, "http://example.com/test.pdf")
        self.assertEqual(publication.bibtex_link, "http://example.com/test.bib")
        self.assertEqual(publication.data_link, "http://example.com/test.data")
        self.assertEqual(publication.sao_nasa_link, "http://example.com/test.sao")
