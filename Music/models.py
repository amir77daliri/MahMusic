from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from mutagen.mp3 import MP3
from Singer.models import Singer
from Album.models import Album
from django.contrib.auth import get_user_model
from django.db.models import Q
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.name}-{ext}'
    return f'Music/images/{final_name}'


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField()


class MusicManager(models.Manager):
    def get_related_songs_with(self, music):
        return self.get_queryset().filter(singer=music.singer).exclude(slug=music.slug)

    def search(self, query):
        lookup = (
            Q(status='A') & (
            Q(name__icontains=query) |
            Q(slug__icontains=query) |
            Q(singer__name__icontains=query) |
            Q(album__name__icontains=query)
            )
        )
        return self.get_queryset().filter(lookup).distinct()


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
    singer = models.ForeignKey(Singer, blank=True, null=True, on_delete=models.SET_NULL, related_name='musics')
    album = models.ForeignKey(Album, blank=True, null=True, on_delete=models.SET_NULL, related_name='musics')

    # Views Fields :
    views = models.PositiveIntegerField(default=1024, blank=True)
    hits = models.ManyToManyField(IPAddress, through="MusicViewsHit", blank=True, related_name='hits')

    # like and save :
    users_like = models.ManyToManyField(get_user_model(), blank=True, related_name='images_liked')
    user_playlist = models.ManyToManyField(get_user_model(), through="PlayList", blank=True, related_name='user_playlist')

    objects = MusicManager()

    class Meta:
        ordering = ['-published_at']

    def thumbnail_tag(self):
        return format_html("<img width=80 height=80 style='border-radius:5px;'src='{}'>".format(self.image.url))
    thumbnail_tag.short_description = "thumbnail"

    def get_views_count(self):
        return self.views #+ self.hits.count()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if not self.music_length:
            time = "{:.2f}".format(MP3(self.music).info.length / 60)
            self.music_length = time
        super(Music, self).save(*args, **kwargs)


class MusicViewsHit(models.Model):
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class PlayList(models.Model):
    user = models.ForeignKey(get_user_model(), blank=True, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
