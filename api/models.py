from django.db import models


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Region(models.Model):
    name = models.CharField(
        max_length=40,
        choices=[
            ("Ophiuchus", "Ophiuchus"),
            ("Lupus", "Lupus"),
            ("UppSco", "UppSco"),
        ],
    )
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Disk(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="disks")

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE, related_name="bands")

    def __str__(self):
        return self.name


class Molecule(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    band = models.ForeignKey(Band, on_delete=models.CASCADE, related_name="molecules")

    def __str__(self):
        return self.name


class Data(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    molecule = models.ForeignKey(
        Molecule, on_delete=models.CASCADE, related_name="data"
    )
    file = models.FileField(upload_to="data/")
    is_viewable = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Data"

    def __str__(self):
        return self.name
