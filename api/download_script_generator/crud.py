from django.core.exceptions import ValidationError

from api.models import Data


def get_data_by_links(links: list[str]) -> list[Data]:
    data_items = Data.objects.filter(filepath__in=links)
    if not data_items.exists():
        raise ValidationError("No data found for the provided links.")
    return data_items
