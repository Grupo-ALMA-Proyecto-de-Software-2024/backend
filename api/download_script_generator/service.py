# content_management/service.py

import logging
import os
from datetime import datetime
from pathlib import Path

from django.conf import settings

from .crud import get_data_by_links
from .generator import generate_download_script

LOGGER = logging.getLogger(__name__)

SCRIPT_TEMPLATE_PATH = Path(__file__).parent / "template.sh"
SCRIPTS_DIR = settings.MEDIA_ROOT / "scripts"
MAX_FILES = 50

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


def generate_download_script_service(links: list[str], total_size_msg: str) -> str:
    data_items = get_data_by_links(links)
    download_links = [data.filepath for data in data_items]

    if not download_links:
        raise ValueError("No valid links found to generate the script.")

    manage_script_directory(directory=SCRIPTS_DIR, max_files=MAX_FILES)

    output_script_path = SCRIPTS_DIR / generate_unique_filename()
    generate_download_script(
        links=download_links,
        total_size_msg=total_size_msg,
        template_path=SCRIPT_TEMPLATE_PATH,
        output_path=output_script_path,
    )

    return str(output_script_path.relative_to(settings.MEDIA_ROOT))
