from django.db import models  # noqa


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
