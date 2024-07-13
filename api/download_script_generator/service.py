# content_management/service.py

import logging
import os
from datetime import datetime
from pathlib import Path

from django.conf import settings

from api.models import Data
from .crud import get_data_by_links
from .generator import generate_download_script

LOGGER = logging.getLogger(__name__)

SCRIPT_TEMPLATE_PATH = Path(__file__).parent / "template.sh"
SCRIPTS_DIR = settings.MEDIA_ROOT / "scripts"
MAX_FILES = 200
BASE_FOLDER_DOWNLOAD_NAME = "AGEPRO_DATA"

SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)


def generate_unique_filename(base_name: str = "download_data") -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.sh"


def manage_script_directory(directory: Path, max_files: int = MAX_FILES) -> None:
    files = sorted(directory.glob("*.sh"), key=os.path.getctime)
    if len(files) > max_files:
        files_to_delete = files[: len(files) - max_files]
        for file in files_to_delete:
            file.unlink()
            LOGGER.info(f"Deleted old script file: {file}")


def size_in_mb_to_human_readable(size_in_mb: float) -> str:
    """Converts a size in MB to a human readable string, e.g. 1.5 MB, 2.3 GB."""
    if size_in_mb < 1:
        return f"{size_in_mb:.2f} MB"
    elif size_in_mb < 1024:
        return f"{size_in_mb:.1f} MB"
    else:
        return f"{size_in_mb / 1024:.1f} GB"


def generate_download_script_service(links: list[str]) -> str:
    data_items = get_data_by_links(links)

    download_links = [data.filepath for data in data_items]
    if not download_links:
        raise ValueError("No valid links found to generate the script.")

    manage_script_directory(directory=SCRIPTS_DIR, max_files=MAX_FILES)

    # Building the total size message
    total_size_in_mb = sum(
        data.size_in_mb for data in data_items if data.size_in_mb is not None
    )
    is_a_size_missing = any(data.size_in_mb is None for data in data_items)
    total_size_msg = (
        f"Total size: {size_in_mb_to_human_readable(total_size_in_mb)}"
        if not is_a_size_missing
        else f"Total size: At least {size_in_mb_to_human_readable(total_size_in_mb)}"
    )

    links_to_targets = {
        data.filepath: f"{BASE_FOLDER_DOWNLOAD_NAME}/{make_data_item_folder_string(data)}"
        for data in data_items
    }

    print(links_to_targets)

    output_script_path = SCRIPTS_DIR / generate_unique_filename()
    generate_download_script(
        url_to_dir_mapping=links_to_targets,
        total_size_msg=total_size_msg,
        template_path=SCRIPT_TEMPLATE_PATH,
        output_path=output_script_path,
    )

    return str(output_script_path.relative_to(settings.MEDIA_ROOT))


def make_data_item_folder_string(data: Data) -> str:
    """Create a string to represent the folder structure for a Data item."""
    return f"{data.region.name}/{data.disk.name}/{data.band.name}/{data.molecule.name}"
