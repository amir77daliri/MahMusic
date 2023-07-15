from django.test import TestCase
from django.core.files import File
from .models import Music

import mock

class MusicTest(TestCase):
    def setUp(self):
        file_mock = mock.MagicMock(spec=File)
        file_mock_image = mock.MagicMock(spec=File)
        file_mock.name = 'test.mp3'
        file_mock_image.name = 'test.png'
        music = Music.objects.create(
            name="test_music",
            status='A',
            music=file_mock,
            image=file_mock_image,
            views=2022,

        )
