from django.urls import path
from .views import SingerList, SingerDetail

app_name = 'singer'
urlpatterns = [
    path('', SingerList.as_view(), name='list'),
    path('<slug:slug>', SingerDetail.as_view(), name='detail')
]
