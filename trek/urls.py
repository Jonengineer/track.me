from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('travel/', include('travel.urls', namespace='Travel')),
    path('user/', include('user.urls', namespace='User')),
    path('', include('appbase.urls', namespace='AppBase'))

]

# Добавь эту строку для обслуживания медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
