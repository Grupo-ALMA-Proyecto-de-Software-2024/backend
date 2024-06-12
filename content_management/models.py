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
    journal_info = models.CharField(max_length=100)
    summary = models.TextField()
    image = models.ImageField(upload_to="publications/")
    pdf_link = models.CharField(max_length=100)
    bibtex_link = models.CharField(max_length=100)
    data_link = models.CharField(max_length=100)
    sao_nasa_link = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PressNews(models.Model):
    OFFICIAL_PRESS = "OP"
    AGEPRO_IN_NEWS = "AN"
    NEWS_TYPES = [
        (OFFICIAL_PRESS, "Official Press"),
        (AGEPRO_IN_NEWS, "AGEPRO in the News"),
    ]

    content = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    news_type = models.CharField(
        max_length=2, choices=NEWS_TYPES, default=OFFICIAL_PRESS
    )

    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = "Press News"
