from django.urls import path
from .views import MusicList, MusicDetail, like_music

app_name = 'music'
urlpatterns = [
    path('', MusicList.as_view(), name='list'),
    path('<slug:slug>', MusicDetail.as_view(), name='detail'),
    path('like/check/', like_music, name='like'),
]
