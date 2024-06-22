import pandas as pd
from django.core.files.uploadedfile import UploadedFile


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


def process_csv_file(datafile: UploadedFile) -> None:
    print("Processing zip file!!!!!!!!!!!")
    data = load_csv_file(datafile)
    print(data)
    print(data.info())
