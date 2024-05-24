from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from alma.admin_site import AlmaAdminSite
from api.models import Region, Disk, Band, Molecule, Data
from content_management.models import CarouselImage, Publication
from content_management.admin import CarouselImageAdmin, PublicationAdmin

admin_site = AlmaAdminSite(name="ALMA Administration")

# core admin
admin_site.register(User, UserAdmin)

# api admin
admin_site.register(Region)
admin_site.register(Disk)
admin_site.register(Band)
admin_site.register(Molecule)
admin_site.register(Data)

# content_management admin
admin_site.register(CarouselImage, CarouselImageAdmin)
admin_site.register(Publication, PublicationAdmin)
