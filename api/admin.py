from django.contrib import admin
from django.utils.html import mark_safe

from .models import CarouselImage


class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date")
    search_fields = ("title", "description")
    list_filter = ("creation_date",)
    readonly_fields = ("image_tag",)

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" height="200" />')
        return "No Image"

    image_tag.short_description = "Image Preview"


admin.site.register(CarouselImage, CarouselImageAdmin)
