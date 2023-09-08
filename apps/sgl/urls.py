from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.Inicio.as_view()), name='index'),
    path('crear_contestado/', login_required(views.ContestadoCreateView.as_view()),
         name='crear_contestado'),
    path('listar_contestado/', login_required(views.ContestadoListView.as_view()),
         name='listar_contestado'),
    path('actualizar_contestado/<uuid:pk>/',
         login_required(views.ContestadoUpdateView.as_view()), name='actualizar_contestado'),
    path('eliminar_contestado/<uuid:pk>/',
         login_required(views.ContestadoDeleteView.as_view()), name='eliminar_contestado'),

    path('listar_aprobado/', login_required(views.AprobadoListView.as_view()),
         name='listar_aprobado'),
    path('actualizar_aprobado/<uuid:pk>/',
         login_required(views.AprobadoUpdateView.as_view()), name='actualizar_aprobado'),
    path('eliminar_aprobado/<uuid:pk>/',
         login_required(views.AprobadoDeleteView.as_view()), name='eliminar_aprobado'),

    path('listar_preparado/', login_required(views.PreparadoListView.as_view()),
         name='listar_preparado'),
    path('actualizar_preparado/<uuid:pk>/',
         login_required(views.PreparadoUpdateView.as_view()), name='actualizar_preparado'),

    path('listar_listo_enviar/', login_required(views.ListoEnviarListView.as_view()),
         name='listar_listo_enviar'),
]
