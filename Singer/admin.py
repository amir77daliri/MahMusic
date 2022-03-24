from django.contrib import admin
from .models import Singer


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ['name', 'thumbnail_tag']
