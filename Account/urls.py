from django.urls import path
from Account import views


app_name = 'account'
urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/info', views.ProfileUpdate.as_view(), name='profile-update'),
    path('search/', views.search, name='search'),
    path('favorit/', views.FavoritMusic.as_view(), name='favorite'),
    path('playlist/', views.PlayListView.as_view(), name='playlist'),
    # Registration and Authentication :
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('active/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_change/', views.change_password, name='password_change'),
    path('password_reset/', views.MyPasswordReset.as_view(), name='password_reset'),
    path('password_reset/done/', views.MyPasswordResetDone.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.MyPasswordResetConfirm.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
