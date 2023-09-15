from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('listado_usuarios/',
         login_required(views.UsuarioListView.as_view()), name='listar_usuario'),
    path('registrar_usuario/',
         login_required(views.UsuarioCreateView.as_view()), name='registrar_usuario'),
]
