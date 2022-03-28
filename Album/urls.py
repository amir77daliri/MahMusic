from django.urls import path
from .views import AlbumList, AlbumDetail

app_name = 'album'
urlpatterns = [
    path('', AlbumList.as_view(), name='list'),
    path('<slug:slug>', AlbumDetail.as_view(), name='detail')
]
