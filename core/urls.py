
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.usuarios.views import Login, logoutUsuario

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.sgl.urls')),
    path('accounts/login/', Login.as_view(), name='login'),
    path('logout/', login_required(logoutUsuario), name='logout')
]
