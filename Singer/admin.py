from django.contrib import admin
from .models import Singer
from Music.models import Music


class MusicInline(admin.StackedInline):
    model = Music
    extra = 0


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ['name', 'thumbnail_tag']
    inlines = [MusicInline]
