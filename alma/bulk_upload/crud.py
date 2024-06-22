from pathlib import Path

from django.core.files import File

from ...api import models


def create_data_from_names(
    region_name: str,
    disk_name: str,
    band_name: str,
    molecule_name: str,
    data_name: str,
    file_path: Path,
) -> models.Data:
    region = models.Region.objects.get(name=region_name)
    if not region:
        raise ValueError(f"Region {region_name} does not exist.")

    disk = models.Disk.filter_disks(
        name=[disk_name],
        regions=[region_name],
    ).first()
    if not disk:
        raise ValueError(f"Disk {disk_name} does not exist in region {region_name}.")

    band = models.Band.filter_bands(
        name=[band_name],
        disks=[disk_name],
        regions=[region_name],
    ).first()
    if not band:
        raise ValueError(
            f"Band {band_name} does not exist in disk {disk_name} and region {region_name}."
        )

    molecule = models.Molecule.filter_molecules(
        name=[molecule_name],
        bands=[band_name],
        disks=[disk_name],
        regions=[region_name],
    ).first()
    if not molecule:
        raise ValueError(
            f"Molecule {molecule_name} does not exist in band {band_name}, disk {disk_name}, and region {region_name}."
        )

    is_viewable = Path(file_path).suffix in [".png", ".jpg", ".jpeg"]
    with open(file_path, "rb") as f:
        data = models.Data.objects.create(
            region=region,
            disk=disk,
            band=band,
            molecule=molecule,
            name=data_name,
            is_viewable=is_viewable,
            file=File(f),
        )
    return data
