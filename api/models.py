import logging
from typing import Optional

from django.db import models
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


class BaseDataModel(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def __str__(self):
        return self.name


class Region(BaseDataModel):
    """A region in the galaxy."""


class Disk(BaseDataModel):
    """A disk in a region of the galaxy."""

    regions = models.ManyToManyField(Region, related_name="disks")

    @classmethod
    def filter_disks(
        cls,
        name: Optional[list[str]] = None,
        regions: Optional[list[str]] = None,
    ):
        disks = cls.objects.all()
        if name:
            disks = disks.filter(name__in=name)
        if regions:
            disks = disks.filter(regions__name__in=regions)
        return disks


class Band(BaseDataModel):
    """A band in a disk of the galaxy."""

    disks = models.ManyToManyField(Disk, related_name="bands")

    @classmethod
    def filter_bands(
        cls,
        name: Optional[list[str]] = None,
        disks: Optional[list[str]] = None,
        regions: Optional[list[str]] = None,
    ):
        bands = cls.objects.select_related("disks__regions").all()
        if name:
            bands = bands.filter(name__in=name)
        if disks:
            bands = bands.filter(disks__name__in=disks)
        if regions:
            bands = bands.filter(disks__regions__name__in=regions)
        return bands


class Molecule(BaseDataModel):
    """A molecule in a band of a disk of the galaxy."""

    bands = models.ManyToManyField(Band, related_name="molecules")

    @classmethod
    def filter_molecules(
        cls,
        name: Optional[list[str]] = None,
        bands: Optional[list[str]] = None,
        disks: Optional[list[str]] = None,
        regions: Optional[list[str]] = None,
    ):
        molecules = cls.objects.select_related("bands__disks__regions").all()
        if name:
            molecules = molecules.filter(name__in=name)
        if bands:
            molecules = molecules.filter(bands__name__in=bands)
        if disks:
            molecules = molecules.filter(bands__disks__name__in=disks)
        if regions:
            molecules = molecules.filter(bands__disks__regions__name__in=regions)
        return molecules


class Data(BaseDataModel):
    """Data associated with a molecule."""

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="data")
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE, related_name="data")
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="data")
    molecule = models.ForeignKey(
        Molecule, on_delete=models.CASCADE, related_name="data"
    )
    file = models.FileField(upload_to="data/")
    is_viewable = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Data"

    def clean(self):
        if self.molecule not in self.band.molecules.all():
            raise ValidationError({"molecule": "Molecule not in band"})
        if self.band not in self.disk.bands.all():
            raise ValidationError({"band": "Band not in disk"})
        if self.disk not in self.region.disks.all():
            raise ValidationError({"disk": "Disk not in region"})

    @classmethod
    def filter_by_name(
        cls,
        name: Optional[list[str]] = None,
        molecule_name: Optional[list[str]] = None,
        band_name: Optional[list[str]] = None,
        disk_name: Optional[list[str]] = None,
        region_name: Optional[list[str]] = None,
    ):
        data = cls.objects.select_related("region", "disk", "band", "molecule").all()
        if name:
            data = data.filter(name__in=name)
        if molecule_name:
            data = data.filter(molecule__name__in=molecule_name)
        if band_name:
            data = data.filter(band__name__in=band_name)
        if disk_name:
            data = data.filter(disk__name__in=disk_name)
        if region_name:
            data = data.filter(region__name__in=region_name)
        return data
