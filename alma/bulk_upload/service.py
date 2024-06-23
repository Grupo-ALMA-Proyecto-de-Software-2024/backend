import pandas as pd
from django.core.files.uploadedfile import UploadedFile

from .crud import create_data_from_names


EXPECTED_COLUMN_TYPES = {
    "region": str,
    "disco": str,
    "banda": str,
    "molecula": str,
    "nombre_dato": str,
    "link_dato": str,
    "visualizable": bool,
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

        data = data.astype(EXPECTED_COLUMN_TYPES)

    except Exception as e:
        raise ValueError(f"Error loading CSV file: {e}")

    return data


def populate_database(data: pd.DataFrame) -> None:
    for row in data.itertuples(index=False):
        create_data_from_names(
            region_name=row.region,
            disk_name=row.disco,
            band_name=row.banda,
            molecule_name=row.molecula,
            data_name=row.nombre_dato,
            file_path=row.link_dato,
            is_viewable=row.visualizable,
        )


def process_csv_file(datafile: UploadedFile) -> None:
    print("Processing zip file!!!!!!!!!!!")
    data = load_csv_file(datafile)
    populate_database(data)
    print("Populated database!!!!!!!!!!!")
