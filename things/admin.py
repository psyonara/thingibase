from django.contrib import admin
from django.contrib.admin import register

from things.models import Thing, File, Image


@register(Thing)
class ThingAdmin(admin.ModelAdmin):
    pass


@register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass


@register(File)
class FileAdmin(admin.ModelAdmin):
    pass
