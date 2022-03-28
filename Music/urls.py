from django.urls import path
from .views import MusicList

app_name = 'music'
urlpatterns = [
    path('', MusicList.as_view(), name='list'),
]
