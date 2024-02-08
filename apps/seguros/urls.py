from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import Inicio, LicitacionDetailView, LicitacionesListView, AprobadasListView, AprobadaDetailView, AprobadaUpdateView, EnviadaListView, EnviadaDetailView, EnviadaUpdateView, LicitacionCreateView, LicitacionUpdateView, LicitacionDeleteView, ListasEnviarListView, ListasEnviarView, ListaEnviarDetailView, PreparadasListView, PreparadaDetailView, PreparadaUpdateView, ObtenerPeritosView, TerminadaListView, TerminadaDetailView

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
        route='detalle_licitacion/<uuid:pk>/',
        view=login_required(LicitacionDetailView.as_view()),
        name='detalle_licitacion'
    ),

    path(
        route='editar_licitacion/<uuid:pk>/',
        view=login_required(LicitacionUpdateView.as_view()),
        name='editar_licitacion'
    ),

    path(
        route='eliminar_licitacion/<uuid:pk>/',
        view=login_required(LicitacionDeleteView.as_view()),
        name='eliminar_licitacion'
    ),

    path(
        route='aprobadas/',
        view=login_required(AprobadasListView.as_view()),
        name='listar_aprobadas'
    ),

    path(
        route='detalle_aprobada/<uuid:pk>/',
        view=login_required(AprobadaDetailView.as_view()),
        name='detalle_aprobada'
    ),

    path(
        route='editar_aprobada/<uuid:pk>/',
        view=login_required(AprobadaUpdateView.as_view()),
        name='editar_aprobada'
    ),

    path(
        route='preparadas/',
        view=login_required(PreparadasListView.as_view()),
        name='listar_preparadas'
    ),

    path(
        route='detalle_preparada/<uuid:pk>/',
        view=login_required(PreparadaDetailView.as_view()),
        name='detalle_preparada'
    ),

    path(
        route='editar_preparada/<uuid:pk>/',
        view=login_required(PreparadaUpdateView.as_view()),
        name='editar_preparada'
    ),

    path(
        route='listar_listasenviar/',
        view=login_required(ListasEnviarListView.as_view()),
        name='listar_listasenviar'
    ),

    path(
        route='enviar_listasenviar/<uuid:lista_id>/',
        view=login_required(ListasEnviarView.as_view()),
        name='enviar_listasenviar'
    ),

    path(
        route='detalle_listaenviar/<uuid:pk>/',
        view=login_required(ListaEnviarDetailView.as_view()),
        name='detalle_listaenviar'
    ),

    path(
        route='enviadas/',
        view=login_required(EnviadaListView.as_view()),
        name='listar_enviadas'
    ),

    path(
        route='detalle_enviada/<uuid:pk>/',
        view=login_required(EnviadaDetailView.as_view()),
        name='detalle_enviada'
    ),

    path(
        route='editar_enviada/<uuid:pk>/',
        view=login_required(EnviadaUpdateView.as_view()),
        name='editar_enviada'
    ),

    path(
        route='terminadas/',
        view=login_required(TerminadaListView.as_view()),
        name='listar_terminadas'
    ),

    path(
        route='detalle_terminada/<uuid:pk>/',
        view=login_required(TerminadaDetailView.as_view()),
        name='detalle_terminada'
    ),

    path(
        route='obtener_peritos/<uuid:aseguradora_id>/',
        view=login_required(ObtenerPeritosView.as_view()),
        name='obtener_peritos'
    )

]
