from django.contrib import admin

from . import models


# Inline tables
class ReadOnlyTabularInline(admin.TabularInline):
    extra = 1

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class DiskInline(ReadOnlyTabularInline):
    model = models.Disk.regions.through


class BandInline(ReadOnlyTabularInline):
    model = models.Band.disks.through


class MoleculeInline(ReadOnlyTabularInline):
    model = models.Molecule.bands.through


class DataInline(ReadOnlyTabularInline):
    model = models.Data


# Admin views
class RegionAdmin(admin.ModelAdmin):
    inlines = (DiskInline,)
    search_fields = ("name",)


class DiskAdmin(admin.ModelAdmin):
    inlines = (BandInline,)
    filter_horizontal = ("regions",)


class BandAdmin(admin.ModelAdmin):
    inlines = (MoleculeInline,)
    filter_horizontal = ("disks",)


class MoleculeAdmin(admin.ModelAdmin):
    inlines = (DataInline,)
    filter_horizontal = ("bands",)


class DataAdmin(admin.ModelAdmin):
    change_list_template = "admin/change_list.html"
