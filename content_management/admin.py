from django.contrib import admin
from django.utils.html import mark_safe


class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date")
    search_fields = ("title", "description")
    list_filter = ("creation_date",)
    readonly_fields = ("image_tag",)
    fields = ("image_tag", "image", "title", "description")

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" height="200" />')
        return "No Image"

    image_tag.short_description = "Image Preview"


class PublicationAdmin(admin.ModelAdmin):
    list_display = ("title", "authors", "journal_info")
    search_fields = ("title", "authors", "journal_info")
    readonly_fields = ("image_tag",)
    fields = (
        "title",
        "authors",
        "full_authors",
        "journal_info",
        "summary",
        "image",
        "image_tag",
        "pdf_link",
        "bibtex_link",
        "data_link",
        "sao_nasa_link",
    )

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" height="200" />')
        return "No Image"

    image_tag.short_description = "Image Preview"
