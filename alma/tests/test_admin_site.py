from django.test import TestCase
from alma.admin_site import sort_models_in_app_list


class SortModelsInAppListTest(TestCase):
    def test_sort_models_in_app_list(self):
        apps = [
            {"name": "API", "models": [{"object_name": "Model2"}, {"object_name": "Model1"}]},
            {"name": "Other", "models": [{"object_name": "ModelA"}, {"object_name": "ModelB"}]},
        ]
        app_name = "API"
        model_order = ["Model1", "Model2"]

        result = sort_models_in_app_list(apps, app_name, model_order)

        self.assertEqual(result[0]["models"], [{"object_name": "Model1"}, {"object_name": "Model2"}])
