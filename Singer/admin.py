from django.contrib import admin
from .models import Singer
from Music.models import Music
from Album.models import Album


class MusicInline(admin.StackedInline):
    model = Music
    extra = 0
    classes = ('collapse',)


class AlbumInline(admin.StackedInline):
    model = Album
    extra = 0
    classes = ('collapse',)


@admin.register(Singer)
class SingerAdmin(admin.ModelAdmin):
    list_display = ['name', 'thumbnail_tag', 'musics_count', 'albums_count']
    inlines = [MusicInline, AlbumInline]

    def musics_count(self, obj):
        return obj.musics.count()

    def albums_count(self, obj):
        return obj.albums.count()
