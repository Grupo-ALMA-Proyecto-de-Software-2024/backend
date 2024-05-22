from django.contrib import admin
from django.utils.html import mark_safe
from markdownify.templatetags.markdownify import markdownify as md


class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date")
    search_fields = ("title", "description")
    list_filter = ("creation_date",)
    readonly_fields = ("image_tag", "markdown_description")
    fields = ("image_tag", "image", "title", "description", "markdown_description")

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" height="200" />')
        return "No Image"

    def markdown_description(self, obj):
        return mark_safe(md(obj.description))

    image_tag.short_description = "Image Preview"
    markdown_description.short_description = "Description"
