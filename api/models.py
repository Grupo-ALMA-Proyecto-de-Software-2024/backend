from django.db import models  # noqa


class CarouselImage(models.Model):
    image = models.ImageField(upload_to="carousel/")
    title = models.CharField(max_length=100)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Data structure
# :arrow_right: Ophiuchus
#         :arrow_right_hook: Disco 1
#                :arrow_right_hook: Banda 6
#                       :arrow_right_hook: Contínuo
#                               :arrow_forward: Measurement Set (zip file)
#                               :arrow_forward: Mapa (fitsfile, visualizable online)
#                       :arrow_right_hook: Molécula 1
#                              :arrow_forward: Measurement Set (zip file)
#                              :arrow_forward: Cubo de canales (zip file)
#                              :arrow_forward: Momento 0 (fitsfile, visualizable online)
#                              :arrow_forward: Momento 1 (fitsfile, visualizable online)
#                       :arrow_right_hook: Molécula 2
#                              :arrow_forward: Measurement Set (zip file)
#                              :arrow_forward: Cubo de canales (zip file)
#                              :arrow_forward: Momento 0 (fitsfile, visualizable online)
#                              :arrow_forward: Momento 1 (fitsfile, visualizable online)
#                       :arrow_right_hook: Molécula N …
#                 :arrow_right_hook: Banda 7
#                      Lo mismo que Banda 6
#         :arrow_right_hook: Disco N …
#                Misma estructura
# :arrow_right:Lupus
#        La misma estructura que para Ophiuchus
# :arrow_right:UppSco
#        La misma estructura que para Ophiuchus (edited)


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


class Disk(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Band(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)


class Molecule(models.Model):
    name = models.CharField(max_length=40)
    creation_date = models.DateTimeField(auto_now_add=True)
    band = models.ForeignKey(Band, on_delete=models.CASCADE)
    file = models.FileField(upload_to="molecules/")
