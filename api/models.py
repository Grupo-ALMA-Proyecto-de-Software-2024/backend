import logging
from typing import Optional

from django.db import models

logger = logging.getLogger(__name__)


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BaseDataModel(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


def filter_by_field(
    queryset: models.QuerySet, field: str, value: str | list[str]
) -> models.QuerySet:
    if value:
        if isinstance(value, str):
            return queryset.filter(**{field: value})
        elif isinstance(value, list):
            return queryset.filter(**{f"{field}__in": value})
    return queryset


class Region(BaseDataModel):
    """A region in the galaxy."""


class Disk(BaseDataModel):
    """A disk in a region of the galaxy."""

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="disks")

    @classmethod
    def filter_disks(
        cls,
        name: Optional[str | list[str]] = None,
        region: Optional[str | list[str]] = None,
    ):
        disks = cls.objects.select_related("region").all()
        disks = filter_by_field(queryset=disks, field="name", value=name)
        disks = filter_by_field(queryset=disks, field="region__name", value=region)
        return disks


class Band(BaseDataModel):
    """A band in a disk of the galaxy."""

    disk = models.ForeignKey(Disk, on_delete=models.CASCADE, related_name="bands")

    @classmethod
    def filter_bands(
        cls,
        name: Optional[str | list[str]] = None,
        disk: Optional[str | list[str]] = None,
        region: Optional[str | list[str]] = None,
    ):
        bands = cls.objects.select_related("disk__region").all()
        bands = filter_by_field(queryset=bands, field="name", value=name)
        bands = filter_by_field(queryset=bands, field="disk__name", value=disk)
        bands = filter_by_field(
            queryset=bands, field="disk__region__name", value=region
        )
        return bands


class Molecule(BaseDataModel):
    """A molecule in a band of a disk of the galaxy."""

    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="molecules")

    @classmethod
    def filter_molecules(
        cls,
        name: Optional[str | list[str]] = None,
        band: Optional[str | list[str]] = None,
        disk: Optional[str | list[str]] = None,
        region: Optional[str | list[str]] = None,
    ):
        molecules = cls.objects.select_related("band__disk__region").all()
        molecules = filter_by_field(queryset=molecules, field="name", value=name)
        molecules = filter_by_field(queryset=molecules, field="band__name", value=band)
        molecules = filter_by_field(
            queryset=molecules, field="band__disk__name", value=disk
        )
        molecules = filter_by_field(
            queryset=molecules, field="band__disk__region__name", value=region
        )
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
        name: Optional[str | list[str]] = None,
        molecule: Optional[str | list[str]] = None,
        band: Optional[str | list[str]] = None,
        disk: Optional[str | list[str]] = None,
        region: Optional[str | list[str]] = None,
    ):
        data = cls.objects.select_related("molecule__band__disk__region").all()
        data = filter_by_field(queryset=data, field="name", value=name)
        data = filter_by_field(queryset=data, field="molecule__name", value=molecule)
        data = filter_by_field(queryset=data, field="molecule__band__name", value=band)
        data = filter_by_field(
            queryset=data, field="molecule__band__disk__name", value=disk
        )
        data = filter_by_field(
            queryset=data, field="molecule__band__disk__region__name", value=region
        )
        return data
