# Generated by Django 3.2.12 on 2022-03-24 14:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Album', '0002_alter_album_singer'),
        ('Singer', '0001_initial'),
        ('Music', '0004_music_album'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='musics', to='Album.album'),
        ),
        migrations.AlterField(
            model_name='music',
            name='singer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='musics', to='Singer.singer'),
        ),
    ]
