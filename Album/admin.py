from django.contrib import admin
from .models import Album
from Music.models import Music


class MusicInlines(admin.StackedInline):
    model = Music
    extra = 0


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'singer', 'thumbnail_tag']
    sortable_by = ('published_at',)
    list_filter = ['singer']
    inlines = [MusicInlines]