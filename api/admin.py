from django.contrib import admin
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from . import models


class CustomFilteredSelectMultiple(FilteredSelectMultiple):
    def __init__(self, verbose_name, is_stacked=False, *args, **kwargs):
        super().__init__(verbose_name, is_stacked, *args, **kwargs)


class DiskAdminForm(forms.ModelForm):
    class Meta:
        model = models.Disk
        fields = "__all__"
        widgets = {
            "regions": CustomFilteredSelectMultiple("Regions", is_stacked=False),
        }


class BandAdminForm(forms.ModelForm):
    class Meta:
        model = models.Band
        fields = "__all__"
        widgets = {
            "disks": CustomFilteredSelectMultiple("Disks", is_stacked=False),
        }


class MoleculeAdminForm(forms.ModelForm):
    class Meta:
        model = models.Molecule
        fields = "__all__"
        widgets = {
            "bands": CustomFilteredSelectMultiple("Bands", is_stacked=False),
        }


# Inline tables
class ReadOnlyTabularInline(admin.TabularInline):
    extra = 1

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
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
    form = DiskAdminForm
    inlines = (BandInline,)


class BandAdmin(admin.ModelAdmin):
    form = BandAdminForm
    inlines = (MoleculeInline,)


class MoleculeAdmin(admin.ModelAdmin):
    form = MoleculeAdminForm
    inlines = (DataInline,)
