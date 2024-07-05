from typing import Optional

from api import models

from django.core.exceptions import ValidationError


def create_data_from_names(
    region_name: str,
    disk_name: str,
    band_name: str,
    molecule_name: str,
    data_name: str,
    filepath: str,
    image_link: Optional[str] = None,
    size_in_mb: Optional[float] = None,
) -> models.Data:
    if models.Data.objects.filter(filepath=filepath).exists():
        raise ValidationError(f"Data with filepath {filepath} already exists")

    # get or create region
    region, _ = models.Region.objects.get_or_create(name=region_name)
    disk, _ = models.Disk.objects.get_or_create(name=disk_name)
    band, _ = models.Band.objects.get_or_create(name=band_name)
    molecule, _ = models.Molecule.objects.get_or_create(name=molecule_name)

    # add relationships
    disk.regions.add(region)
    band.disks.add(disk)
    molecule.bands.add(band)

    # create data
    data = models.Data(
        region=region,
        disk=disk,
        band=band,
        molecule=molecule,
        name=data_name,
        filepath=filepath,
        image_link=image_link,
        size_in_mb=size_in_mb,
    )
    data.save()
    return data
