import logging
from typing import Optional

from django.db import models
from django.core.exceptions import FieldDoesNotExist

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

    @classmethod
    def filter_objects(cls, related_fields: list[str], **kwargs):
        queryset = cls.objects.select_related(*related_fields)
        for key, value in kwargs.items():
            if value is not None:
                fields = key.split("__")
                try:
                    for field in fields:
                        cls._meta.get_field(field)
                    queryset = queryset.filter(**{key: value})
                except FieldDoesNotExist:
                    logger.warning(
                        f"Trying to filter on non-existent field '{field}' in {cls.__name__}."
                    )
                    continue
        return queryset


class Region(BaseDataModel):
    """A region in the galaxy."""


class Disk(BaseDataModel):
    """A disk in a region of the galaxy."""

    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="disks")

    @classmethod
    def filter_disks(cls, name: Optional[str] = None, region: Optional[str] = None):
        return super().filter_objects(
            related_fields=["region"],
            name=name,
            region__name=region,
        )


class Band(BaseDataModel):
    """A band in a disk of the galaxy."""

    disk = models.ForeignKey(Disk, on_delete=models.CASCADE, related_name="bands")

    @classmethod
    def filter_bands(
        cls,
        name: Optional[str] = None,
        disk: Optional[str] = None,
        region: Optional[str] = None,
    ):
        return super().filter_objects(
            related_fields=["disk", "disk__region"],
            name=name,
            disk__name=disk,
            disk__region__name=region,
        )


class Molecule(BaseDataModel):
    """A molecule in a band of a disk of the galaxy."""

    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="molecules")

    @classmethod
    def filter_molecules(
        cls,
        name: Optional[str] = None,
        band: Optional[str] = None,
        disk: Optional[str] = None,
        region: Optional[str] = None,
    ):
        return super().filter_objects(
            related_fields=["band", "band__disk", "band__disk__region"],
            name=name,
            band__name=band,
            band__disk__name=disk,
            band__disk__region__name=region,
        )


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
        name: Optional[str] = None,
        molecule: Optional[str] = None,
        band: Optional[str] = None,
        disk: Optional[str] = None,
        region: Optional[str] = None,
    ):
        return super().filter_objects(
            related_fields=["molecule", "molecule__band", "molecule__band__disk"],
            name=name,
            molecule__name=molecule,
            molecule__band__name=band,
            molecule__band__disk__name=disk,
            molecule__band__disk__region__name=region,
        )
