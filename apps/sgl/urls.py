from django.urls import path
from . import views
urlpatterns = [
    path('', views.ContestadoView.as_view(), name='contestado'),
    path('aprobado/', views.AprobadoView.as_view(), name='aprobado'),
    path('preparado/', views.PreparacionView.as_view(), name='preparado'),
    path('listo-enviar/', views.ListoEnviarView.as_view(), name='listo_enviar'),
]
