from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import Inicio, LicitacionesListView, AprobadasListView, AprobadaUpdateView, LicitacionCreateView, LicitacionUpdateView, LicitacionDeleteView, ObtenerPeritosView

app_name = 'apps.seguros'

urlpatterns = [

    path(
        route='',
        view=login_required(Inicio.as_view()),
        name='inicio'
    ),
    
    path(
        route='licitaciones/',
        view=login_required(LicitacionesListView.as_view()),
        name='listar_licitaciones'
    ),

    path(
        route='crear_licitacion/',
        view=login_required(LicitacionCreateView.as_view()),
        name='crear_licitacion'
    ),

    path(
        route='editar_licitacion/<uuid:pk>',
        view=login_required(LicitacionUpdateView.as_view()),
        name='editar_licitacion'
    ),

    path(
        route='eliminar_licitacion/<uuid:pk>',
        view=login_required(LicitacionDeleteView.as_view()),
        name='eliminar_licitacion'
    ),

    path(
        route='aprobadas/',
        view=login_required(AprobadasListView.as_view()),
        name='listar_aprobadas'
    ),

    path(
        route='editar_aprobada/<uuid:pk>',
        view=login_required(AprobadaUpdateView.as_view()),
        name='editar_aprobada'
    ),

    # path(
    #     route='buscar/',
    #     view=BuscarListView.as_view(),
    #     name='busqueda'
    # ),

    # path(
    #     route='detalle_contestado/<uuid:uuid>/',
    #     view=login_required(ContestadoDetailView.as_view()),
    #     name='detalle_contestado'
    # ),

    # path(
    #     route='editar_contestado/<uuid:uuid>/',
    #     view=login_required(ContestadoUpdateView.as_view()),
    #     name='editar_contestado'
    # ),

    path(
        route='obtener_peritos/<uuid:aseguradora_id>/',
        view=login_required(ObtenerPeritosView.as_view()),
        name='obtener_peritos'
    )

]
