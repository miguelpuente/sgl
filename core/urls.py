from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.usuarios.views import Login, logoutUsuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('usuarios/', include('apps.usuarios.url')),
    path('', include('apps.sgl.urls')),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', login_required(logoutUsuario), name='logout')
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
