from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views


app_name = 'AppBase'

urlpatterns = [
    path('', views.base_page, name='base_page'),
]

# Добавь эту строку для обслуживания медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)