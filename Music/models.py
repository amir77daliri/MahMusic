from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from mutagen.mp3 import MP3
from Singer.models import Singer
from Album.models import Album
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.name}-{ext}'
    return f'Music/images/{final_name}'


class Music(models.Model):
    STATUS_CHOICES = (
        ('p', 'Pending'),
        ('A', 'Accept')
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='A')
    music = models.FileField(upload_to='Music/songs')
    music_length = models.FloatField(blank=True, default=0)
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    # Relation fields :
    singer = models.ForeignKey(Singer, blank=True, null=True, on_delete=models.SET_NULL)
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-published_at']

    def thumbnail_tag(self):
        return format_html("<img width=80 height=80 style='border-radius:5px;'src='{}'>".format(self.image.url))
    thumbnail_tag.short_description = "thumbnail"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        time = "{:.2f}".format(MP3(self.music).info.length / 60)
        self.music_length = time
        super(Music, self).save(*args, **kwargs)

