from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('userprofile/', views.user_profile, name='user_profile'),
    path('CreateUser/', views.create_user, name='create_user'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_log_out, name='user_log_out'),
]