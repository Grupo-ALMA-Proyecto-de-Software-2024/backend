import logging

import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ValidationError

from .crud import create_data_from_names


LOGGER = logging.getLogger(__name__)


class BulkUploadError(Exception):
    pass


EXPECTED_COLUMN_TYPES = {
    "region": str,
    "disco": str,
    "banda": str,
    "molecula": str,
    "nombre_dato": str,
    "link_dato": str,
    "link_imagen": str,
    "tamaño_mb": float,
}


def process_title(title: str) -> str:
    return title.strip().replace(" ", "_").lower()


def load_csv_file(datafile: UploadedFile) -> pd.DataFrame:
    try:
        data = pd.read_csv(datafile)

        headers = [process_title(header) for header in data.columns]
        data.columns = headers

        missing_columns = set(EXPECTED_COLUMN_TYPES.keys()) - set(data.columns)
        if missing_columns:
            raise ValueError(f"Missing columns: {missing_columns}")

        # strip all strings
        for column in data.columns:
            if data[column].dtype == "object":
                data[column] = data[column].str.strip()

        data = data.astype(EXPECTED_COLUMN_TYPES)

    except Exception as e:
        raise BulkUploadError(f"Error loading CSV file: {e}")

    return data


def populate_database(data: pd.DataFrame) -> None:
    for row in data.itertuples(index=False):
        try:
            create_data_from_names(
                region_name=row.region,
                disk_name=row.disco,
                band_name=row.banda,
                molecule_name=row.molecula,
                data_name=row.nombre_dato,
                filepath=row.link_dato,
                image_link=row.link_imagen,
                size_in_mb=row.tamaño_mb,
            )
        except ValidationError as e:
            raise BulkUploadError(f"Error creating data: {e}")
        except Exception as e:
            raise BulkUploadError(f"Error creating data: {e}")


def process_csv_file(datafile: UploadedFile) -> None:
    LOGGER.info("Processing zip file")
    data = load_csv_file(datafile)
    LOGGER.info("Populating database")
    populate_database(data)
    LOGGER.info("Database populated")
