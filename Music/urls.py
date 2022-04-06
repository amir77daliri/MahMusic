from django.urls import path
from .views import (
    MusicList,
    MusicDetail,
    like_music,
    add_to_playlist,
    del_from_favorite,
    del_from_playlist
)

app_name = 'music'
urlpatterns = [
    path('', MusicList.as_view(), name='list'),
    path('<slug:slug>', MusicDetail.as_view(), name='detail'),
    path('like/check/', like_music, name='like'),
    path('save/check/', add_to_playlist, name='save'),
    path('del-favorite/', del_from_favorite, name='del_favorite'),
    path('del-playlist/', del_from_playlist, name='del_playlist'),
]
