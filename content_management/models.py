from django.db import models


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Publication(models.Model):
    title = models.CharField(max_length=100)
    authors = models.CharField(max_length=100)
    full_authors = models.CharField(max_length=100)
    journalInfo = models.CharField(max_length=100)
    summary = models.TextField()
    image = models.ImageField(upload_to="publications/")
    pdfLink = models.CharField(max_length=100)
    bibtexLink = models.CharField(max_length=100)
    dataLink = models.CharField(max_length=100)
    saoNasaLink = models.CharField(max_length=100)

    def __str__(self):
        return self.title
