import logging
from pathlib import Path


LOGGER = logging.getLogger(__name__)

SCRIPT_GENERATOR_DIR = Path(__file__).parent.resolve()
TEMPLATE_PATH = SCRIPT_GENERATOR_DIR / "template.sh"
OUTPUT_PATH = SCRIPT_GENERATOR_DIR / "download_data.sh"


def generate_download_script(
    url_to_dir_mapping: dict[str, str],
    total_size_msg: str,
    template_path: Path | str = TEMPLATE_PATH,
    output_path: Path | str = OUTPUT_PATH,
) -> None:
    """
    Generate a bash script to download files from a list of links.
    Args:
        links (list[str]): List of links to download.
        total_size_msg (str): Message to display the total size of the files to download.
        template_path (Path | str, optional): Path to the template file. Defaults to TEMPLATE_PATH.
        output_path (Path | str, optional): Path to the output file. Defaults to OUTPUT_PATH.
    """
    if not url_to_dir_mapping:
        LOGGER.warning("No links to download.")
        return

    if not Path(template_path).exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    if Path(output_path).exists():
        LOGGER.warning(
            f"Output file already exists and will be overwritten: {output_path}"
        )

    with open(template_path) as f:
        template = f.read()

    url_to_dir_mapping_str = "\n".join(
        [
            f'LINKS_TO_TARGETS["{url}"]="{dir}"'
            for url, dir in url_to_dir_mapping.items()
        ]
    )
    script = template.replace(
        '"<<url_to_dir_mapping>>"',
        url_to_dir_mapping_str,
    ).replace(
        "<<size>>",
        total_size_msg,
    )

    with open(output_path, "w") as f:
        f.write(script)
