from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include(('apps.users.urls'), namespace='auth')),
    path('', include(('apps.seguros.urls'), namespace='seguros'))
]

# Configuración para servir archivos de medios durante el desarrollo
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
