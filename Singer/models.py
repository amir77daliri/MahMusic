from django.db import models
from django.utils.text import slugify
from django.utils.html import format_html
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f'{instance.name}-{ext}'
    return f'Singer/images/{final_name}'


class Singer(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def thumbnail_tag(self):
        return format_html("<img width=80 height=80 style='border-radius:5px;'src='{}'>".format(self.image.url))
    thumbnail_tag.short_description = "thumbnail"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Singer, self).save(*args, **kwargs)

