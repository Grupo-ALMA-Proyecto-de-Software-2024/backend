from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from alma.admin_site import AlmaAdminSite
from api.models import Region, Disk, Band, Molecule, Data
from api.admin import RegionAdmin, DiskAdmin, BandAdmin, MoleculeAdmin
from content_management.models import CarouselImage, Publication
from content_management.admin import CarouselImageAdmin, PublicationAdmin

admin_site = AlmaAdminSite(name="ALMA Administration")

# core admin
admin_site.register(User, UserAdmin)

# api admin
admin_site.register(Region, RegionAdmin)
admin_site.register(Disk, DiskAdmin)
admin_site.register(Band, BandAdmin)
admin_site.register(Molecule, MoleculeAdmin)
admin_site.register(Data)

# content_management admin
admin_site.register(CarouselImage, CarouselImageAdmin)
admin_site.register(Publication, PublicationAdmin)
