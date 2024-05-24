import logging
from typing import Optional

from django.db import models

logger = logging.getLogger(__name__)


class BaseDataModel(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Region(BaseDataModel):
    """A region in the galaxy."""


class Disk(BaseDataModel):
    """A disk in a region of the galaxy."""

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="disks")

    @classmethod
    def filter_disks(
        cls,
        name: Optional[list[str]] = None,
        region: Optional[list[str]] = None,
    ):
        disks = cls.objects.select_related("region").all()
        if name:
            disks = disks.filter(name__in=name)
        if region:
            disks = disks.filter(region__name__in=region)
        return disks


class Band(BaseDataModel):
    """A band in a disk of the galaxy."""

    disk = models.ForeignKey(Disk, on_delete=models.CASCADE, related_name="bands")

    @classmethod
    def filter_bands(
        cls,
        name: Optional[list[str]] = None,
        disk: Optional[list[str]] = None,
        region: Optional[list[str]] = None,
    ):
        bands = cls.objects.select_related("disk__region").all()
        if name:
            bands = bands.filter(name__in=name)
        if disk:
            bands = bands.filter(disk__name__in=disk)
        if region:
            bands = bands.filter(disk__region__name__in=region)
        return bands


class Molecule(BaseDataModel):
    """A molecule in a band of a disk of the galaxy."""

    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="molecules")

    @classmethod
    def filter_molecules(
        cls,
        name: Optional[list[str]] = None,
        band: Optional[list[str]] = None,
        disk: Optional[list[str]] = None,
        region: Optional[list[str]] = None,
    ):
        molecules = cls.objects.select_related("band__disk__region").all()
        if name:
            molecules = molecules.filter(name__in=name)
        if band:
            molecules = molecules.filter(band__name__in=band)
        if disk:
            molecules = molecules.filter(band__disk__name__in=disk)
        if region:
            molecules = molecules.filter(band__disk__region__name__in=region)
        return molecules


class Data(BaseDataModel):
    """Data associated with a molecule."""

    molecule = models.ForeignKey(
        Molecule, on_delete=models.CASCADE, related_name="data"
    )
    file = models.FileField(upload_to="data/")
    is_viewable = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Data"

    @classmethod
    def filter_data(
        cls,
        name: Optional[list[str]] = None,
        molecule: Optional[list[str]] = None,
        band: Optional[list[str]] = None,
        disk: Optional[list[str]] = None,
        region: Optional[list[str]] = None,
    ):
        data = cls.objects.select_related("molecule__band__disk__region").all()
        if name:
            data = data.filter(name__in=name)
        if molecule:
            data = data.filter(molecule__name__in=molecule)
        if band:
            data = data.filter(molecule__band__name__in=band)
        if disk:
            data = data.filter(molecule__band__disk__name__in=disk)
        if region:
            data = data.filter(molecule__band__disk__region__name__in=region)
        return data
