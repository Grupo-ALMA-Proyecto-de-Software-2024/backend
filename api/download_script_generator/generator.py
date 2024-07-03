import logging
from pathlib import Path

LOGGER = logging.getLogger(__name__)

SCRIPT_GENERATOR_DIR = Path(__file__).parent.resolve()
TEMPLATE_PATH = SCRIPT_GENERATOR_DIR / "template.sh"
OUTPUT_PATH = SCRIPT_GENERATOR_DIR / "download_data.sh"


def generate_download_script(
    links: list[str],
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
    if not links:
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

    links_str = "\n".join([f'"{link}"' for link in links])
    script = template.replace('    "<<links>>"', links_str).replace(
        "<<size>>", total_size_msg
    )

    with open(output_path, "w") as f:
        f.write(script)


generate_download_script(
    links=[
        "ftp://ftp.cv.nrao.edu/NRAO-staff/rloomis/MAPS/HD_163296/images/13CO/robust_0.5/HD_163296_13CO_110GHz.robust_0.5.JvMcorr.image.pbcor.fits",
        "ftp://ftp.cv.nrao.edu/NRAO-staff/rloomis/MAPS/HD_163296/images/13CO/robust_0.5/HD_163296_13CO_220GHz.robust_0.5.image.pbcor.fits",
        "ftp://ftp.cv.nrao.edu/NRAO-staff/rloomis/MAPS/HD_163296/images/13CO/robust_0.5/HD_163296_13CO_220GHz.robust_0.5.JvMcorr.image.fits ",
    ],
    total_size_msg="Total size: <X> MB",
)
