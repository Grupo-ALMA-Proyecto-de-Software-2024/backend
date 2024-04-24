from django.test import TestCase
from alma.admin_site import find_app, update_apps_layout


class AdminSiteTest(TestCase):
    def test_find_app(self):
        apps = {
            "API": {
                "name": "API",
                "models": [
                    {"name": "Model1"},
                    {"name": "Model2"},
                ],
            },
            "Other": {
                "name": "Other",
                "models": [
                    {"name": "ModelA"},
                    {"name": "ModelB"},
                ],
            },
        }
        app_name = "API"

        result = find_app(apps, app_name)

        self.assertEqual(
            result, {"name": "API", "models": [{"name": "Model1"}, {"name": "Model2"}]}
        )

    def test_update_apps_layout(self):
        apps = {
            "API": {
                "name": "API",
                "models": [
                    {"name": "Model1"},
                    {"name": "Model2"},
                ],
            },
            "Other": {
                "name": "Other",
                "models": [
                    {"name": "ModelA"},
                    {"name": "ModelB"},
                ],
            },
        }
        template = [
            {
                "app_backend_name": "API",
                "name_to_display": "API-DISPLAY",
                "models": ["Model2", "Model1"],
            }
        ]

        result = update_apps_layout(apps, template)

        self.assertEqual(
            result["API"]["models"],
            [{"name": "Model2"}, {"name": "Model1"}],
        )
