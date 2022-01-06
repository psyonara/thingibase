from django.contrib import admin
from django.contrib.admin import register

from things.models import Thing


@register(Thing)
class ThingAdmin(admin.ModelAdmin):
    pass
