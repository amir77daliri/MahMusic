from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import os
# Create your models here.



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance , filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.name}-{instance.pk}{ext}'
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
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Music, self).save(*args, **kwargs)

