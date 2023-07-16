from django.test import TestCase
from .models import Music
from django.core.files.uploadedfile import SimpleUploadedFile


class MusicModelTest(TestCase):
    def setUp(self) -> None:
        mp3_file = SimpleUploadedFile("test_file.mp3", b"test content", content_type="audio/mpeg")
        jpg_file = SimpleUploadedFile("test_image.jpg", b"test content", content_type="image/jpeg")
        music1 = Music.objects.create(
            name="test_music",
            music=mp3_file,
            music_length=4.6,
            image=jpg_file,
            views=1377
        )

    def test_get_views(self):
        music = Music.objects.get(name="test_music")
        self.assertEqual(music.get_views_count(), 1374)