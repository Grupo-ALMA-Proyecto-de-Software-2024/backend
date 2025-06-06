from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from ..models import PressNews


class PressNewsViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.press_news_1 = PressNews.objects.create(
            content="Test content 1",
            news_type=PressNews.OFFICIAL_PRESS,
        )

        self.press_news_2 = PressNews.objects.create(
            content="Test content 2",
            news_type=PressNews.AGEPRO_IN_NEWS,
        )

    def test_press_news_list(self):
        response = self.client.get(reverse("backend:press-news"))
        response_data = response.data["press_news"]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)

        self.assertEqual(response_data[0]["content"], self.press_news_1.content)
        self.assertEqual(response_data[0]["news_type"], self.press_news_1.news_type)
        self.assertIsNotNone(response_data[0]["creation_date"])

        self.assertEqual(response_data[1]["content"], self.press_news_2.content)
        self.assertEqual(response_data[1]["news_type"], self.press_news_2.news_type)
        self.assertIsNotNone(response_data[1]["creation_date"])

    def test_press_news_fields(self):
        press_news_1 = PressNews.objects.get(id=self.press_news_1.id)
        self.assertEqual(press_news_1.content, "Test content 1")
        self.assertEqual(press_news_1.news_type, PressNews.OFFICIAL_PRESS)

        press_news_2 = PressNews.objects.get(id=self.press_news_2.id)
        self.assertEqual(press_news_2.content, "Test content 2")
        self.assertEqual(press_news_2.news_type, PressNews.AGEPRO_IN_NEWS)
