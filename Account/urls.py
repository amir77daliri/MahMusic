from django.urls import path
from Account import views


app_name = 'account'
urlpatterns = [
    path('profile/', views.Profile.as_view(), name='profile'),
    path('profile/info', views.ProfileUpdate.as_view(), name='profile-update'),

    # Registration and Authentication :
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('active/<uidb64>/<token>/', views.activate, name='activate'),
    path('password_change/', views.change_password, name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
