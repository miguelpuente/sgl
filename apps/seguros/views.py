from django.contrib.auth.mixins import UserPassesTestMixin
from django import forms
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.utils import timezone
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Licitacion, Aprobada, Preparada, ListaEnviar, Enviada, Perito
from apps.direccion.models import DatoEntrega, Provincia, Localidad
from .forms import EnviadaForm, LicitacionForm, AprobadaForm, PreparadaForm

class Inicio(TemplateView):
    template_name = 'pages/home.html'


class LicitacionesListView(ListView):
    model = Licitacion
    queryset = Licitacion.objects.filter(activo=True, terminado=False)
    context_object_name = 'licitaciones'
    template_name = 'pages/licitaciones/listar_licitaciones.html'
    # Con ajax - no tiene formato
    # template_name = 'includes/componentes/listado.html'
    ordering = ('-creado',)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     data = {}
    #     try:
    #         accion = request.POST['accion']
    #         if accion == 'buscar_perito_id':
    #             data = [{'id':'', 'text':'---------'}]
    #             for perito in Perito.objects.filter(aseguradora_id=request.POST['id']):
    #                 data.append({'id': perito.id, 'text': perito.nombre})
    #         else:
    #             data['error'] = 'Ha ocurrido un error al cargar las licitaciones'
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Licitaciones"
        context["card_title"] = "Licitaciones contestadas esperando Aprobación"
        context["list_url"] = reverse_lazy('seguros:listar_licitaciones')
        return context
    

class LicitacionCreateView(CreateView):
    model = Licitacion
    form_class = LicitacionForm
    template_name = 'pages/licitaciones/crear_licitacion.html'
    success_url = reverse_lazy('seguros:listar_licitaciones')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'agregar':
                form = self.get_form()
                if form.is_valid():
                    # Crea el objeto DatoEntrega
                    nuevo_dato_entrega = DatoEntrega.objects.create(localidad=form.cleaned_data['localidad'])
                    # Guarda el objeto DatoEntrega
                    nuevo_dato_entrega.save()
                    # Asigna el objeto DatoEntrega al campo datos_entrega
                    form.instance.datos_entrega = nuevo_dato_entrega

                    data = form.save()
                else:
                    # En el caso de errores, incluir detalles en el diccionario 'data'
                    data['error'] = 'NO se guardó la licitación'
                    data['form_errors'] = form.errors
            elif accion == 'buscar_perito_id':
                data = []
                for perito in Perito.objects.filter(aseguradora_id=request.POST['id']):
                    data.append({'id': perito.id, 'nombre': perito.nombre})
                return JsonResponse(data, safe=False)
            elif accion == 'buscar_localidad_id':
                data = []
                for localidad in Localidad.objects.filter(provincia_id=request.POST['id']):
                    data.append({'id': localidad.id, 'nombre': localidad.localidad})
                return JsonResponse(data, safe=False)
            else:
                data['error'] = 'NO ha ingresado una acción válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Licitaciones"
        context["card_title"] = "Crear Licitación"
        context["accion"] = "agregar"
        context["list_url"] = reverse_lazy('seguros:listar_licitaciones')
        return context


class LicitacionDetailView(DetailView):
    model = Licitacion
    template_name = 'pages/licitaciones/detalle_licitacion.html'
    context_object_name = 'licitacion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Detalle Licitación"
        context["card_title"] = f"Siniestro - {self.object.numero_siniestro}"
        context["list_url"] = reverse_lazy('seguros:listar_licitaciones')
        return context


class LicitacionUpdateView(UserPassesTestMixin, UpdateView):
    model = Licitacion
    form_class = LicitacionForm
    template_name = 'pages/licitaciones/crear_licitacion.html'
    success_url = reverse_lazy('seguros:listar_licitaciones')

    def test_func(self):
        grupos = ['SUPERVISOR','GERENTE_SUCURSAL']  # Lista de nombres de grupos a verificar
        pertenece_a_admin_sucursal = any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) and self.request.user.perfil.sucursal == self.get_object().sucursal 
        return self.request.user.is_authenticated and (pertenece_a_admin_sucursal or self.request.user == self.get_object().user or self.request.user.groups.filter(name='GERENTE_GENERAL').exists())

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'editar':
                form = self.get_form()
                if form.is_valid():
                    # Mantener al mismo usuario creador si no es el que está editando
                    if self.request.user != self.get_object().user:
                        form.instance.user = self.get_object().user

                    localidad = DatoEntrega.objects.get(id = form.instance.datos_entrega_id)
                    localidad.localidad = form.cleaned_data['localidad']
                    localidad.save()

                    if not Aprobada.objects.filter(licitacion=form.instance) and form.instance.terminado == True:
                        Aprobada.objects.create(licitacion=form.instance).save()
                        
                    data = form.save()
                else:
                    # En el caso de errores, incluir detalles en el diccionario 'data'
                    data['error'] = 'NO se guardó la licitación'
                    data['form_errors'] = form.errors
                    print(form.errors)
            elif accion == 'buscar_perito_id':
                data = []
                for perito in Perito.objects.filter(aseguradora_id=request.POST['id']):
                    data.append({'id': perito.id, 'nombre': perito.nombre})
                return JsonResponse(data, safe=False)
            elif accion == 'buscar_localidad_id':
                data = []
                for localidad in Localidad.objects.filter(provincia_id=request.POST['id']):
                    data.append({'id': localidad.id, 'nombre': localidad.localidad})
                return JsonResponse(data, safe=False)

            else:
                data['error'] = 'NO ha ingresado una acción válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Licitaciones"
        context["card_title"] = "Editar Licitación"
        context["accion"] = "editar"
        context["list_url"] = reverse_lazy('seguros:listar_licitaciones')
        return context


class LicitacionDeleteView(UserPassesTestMixin, DeleteView):
    model = Licitacion
    template_name = 'pages/licitaciones/eliminar_licitacion.html'
    success_url = reverse_lazy('seguros:listar_licitaciones')

    def test_func(self):
        grupos = ['SUPERVISOR','GERENTE_SUCURSAL']  # Lista de nombres de grupos a verificar
        pertenece_a_admin_sucursal = any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) and self.request.user.perfil.sucursal == self.get_object().sucursal 
        return self.request.user.is_authenticated and (pertenece_a_admin_sucursal or self.request.user == self.get_object().user or self.request.user.groups.filter(name='GERENTE_GENERAL').exists())

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Licitaciones"
        context["card_title"] = "Eliminar Licitación"
        context["list_url"] = reverse_lazy('seguros:listar_licitaciones')
        return context


class AprobadasListView(ListView):
    model = Aprobada
    queryset = Aprobada.objects.filter(activo=True, terminado=False, licitacion__terminado=True, licitacion__activo=True)
    context_object_name = 'aprobadas'
    template_name = 'pages/aprobadas/listar_aprobadas.html'
    ordering = ('-creado',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Aprobadas"
        context["card_title"] = "Licitaciones aprobadas esperando preparación"
        context["list_url"] = reverse_lazy('seguros:listar_aprobadas')
        return context


class AprobadaDetailView(DetailView):
    model = Aprobada
    template_name = 'pages/aprobadas/detalle_aprobada.html'
    context_object_name = 'aprobada'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Detalle Aprobada"
        context["card_title"] = f"Siniestro - {self.object.licitacion.numero_siniestro}"
        context["list_url"] = reverse_lazy('seguros:listar_aprobadas')
        return context


class AprobadaUpdateView(UserPassesTestMixin, UpdateView):
    model = Aprobada
    form_class = AprobadaForm
    template_name = 'pages/aprobadas/editar_aprobada.html'
    success_url = reverse_lazy('seguros:listar_aprobadas')

    def test_func(self):
        grupos = ['SUPERVISOR','GERENTE_SUCURSAL']  # Lista de nombres de grupos a verificar
        pertenece_a_admin_sucursal = any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) and self.request.user.perfil.sucursal == self.get_object().licitacion.sucursal 
        return self.request.user.is_authenticated and (pertenece_a_admin_sucursal or self.request.user == self.get_object().licitacion.user or self.request.user.groups.filter(name='GERENTE_GENERAL').exists())

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'editar':
                form = self.get_form()
                if form.is_valid():
                    if not Preparada.objects.filter(aprobada=form.instance) and form.instance.terminado == True:
                        Preparada.objects.create(aprobada=form.instance).save()
                    data = form.save()
                else:
                    # En el caso de errores, incluir detalles en el diccionario 'data'
                    data['error'] = 'NO se guardó la licitación'
                    data['form_errors'] = form.errors
            else:
                data['error'] = 'NO ha ingresado una acción válida'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Aprobadas"
        context["card_title"] = f"Editar Siniestro - { self.get_object().licitacion.numero_siniestro}"
        context["accion"] = "editar"
        context["list_url"] = reverse_lazy('seguros:listar_aprobadas')
        return context


class PreparadasListView(ListView):
    model = Preparada
    queryset = Preparada.objects.filter(activo=True, terminado=False, aprobada__terminado=True, aprobada__activo=True)
    context_object_name = 'preparadas'
    template_name = 'pages/preparadas/listar_preparadas.html'
    ordering = ('-creado',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "En Preparación"
        context["card_title"] = "Licitaciones en preparación"
        context["list_url"] = reverse_lazy('seguros:listar_preparadas')

        for preparada in context['preparadas']:
            # Suma 5 días a la fecha_aprobado
            entrega = preparada.aprobada.licitacion.demora.dia
            preparada.nueva_fecha = preparada.aprobada.fecha_aprobado + timedelta(days=entrega)

            # Convierte la fecha actual a datetime
            fecha_actual = timezone.now().date()

            # Calcula la diferencia de días
            preparada.dias_restantes = (preparada.nueva_fecha - fecha_actual).days
        return context


class PreparadaDetailView(DetailView):
    model = Preparada
    template_name = 'pages/preparadas/detalle_preparada.html'
    context_object_name = 'preparada'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Detalle En preparación"
        context["card_title"] = f"Siniestro - {self.object.aprobada.licitacion.numero_siniestro}"
        context["list_url"] = reverse_lazy('seguros:listar_preparadas')
        return context


class PreparadaUpdateView(UserPassesTestMixin, UpdateView):
    model = Preparada
    form_class = PreparadaForm
    template_name = 'pages/preparadas/editar_preparada.html'
    success_url = reverse_lazy('seguros:listar_preparadas')

    def test_func(self):
        grupos = ['SUPERVISOR','GERENTE_SUCURSAL']  # Lista de nombres de grupos a verificar
        pertenece_a_admin_sucursal = any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) and self.request.user.perfil.sucursal == self.get_object().aprobada.licitacion.sucursal 
        return self.request.user.is_authenticated and (pertenece_a_admin_sucursal or self.request.user == self.get_object().aprobada.licitacion.user or self.request.user.groups.filter(name='GERENTE_GENERAL').exists())

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'editar':
                form = self.get_form()
                if form.is_valid():
                    if not ListaEnviar.objects.filter(preparada=form.instance) and form.instance.terminado == True:
                        ListaEnviar.objects.create(preparada=form.instance).save()
                    data = form.save()
                else:
                    # En el caso de errores, incluir detalles en el diccionario 'data'
                    data['error'] = 'NO se guardó la licitación'
                    data['form_errors'] = form.errors
            else:
                data['error'] = 'NO ha ingresado una acción válida'
        except forms.ValidationError as e:
            data['error'] = str(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "En Preparación"
        context["card_title"] = f"Editar Siniestro - { self.get_object().aprobada.licitacion.numero_siniestro}"
        context["accion"] = "editar"
        context["list_url"] = reverse_lazy('seguros:listar_preparadas')
        context["articulos"] = self.get_object().aprobada.licitacion.cantidad_articulos
        return context


class ListasEnviarListView(ListView):
    model = ListaEnviar
    queryset = ListaEnviar.objects.filter(activo=True, terminado=False, preparada__terminado=True, preparada__activo=True)
    context_object_name = 'listasenviar'
    template_name = 'pages/listasenviar/listar_listasenviar.html'
    ordering = ('-creado',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Listas para Enviar"
        context["card_title"] = "Licitaciones listas para enviar"
        context["list_url"] = reverse_lazy('seguros:listar_listasenviar')
        
        for lista in context['listasenviar']:
            # Suma 5 días a la fecha_aprobado
            entrega = lista.preparada.aprobada.licitacion.demora.dia
            lista.nueva_fecha = lista.preparada.aprobada.fecha_aprobado + timedelta(days=entrega)

            # Convierte la fecha actual a datetime
            fecha_actual = timezone.now().date()

            # Calcula la diferencia de días
            lista.dias_restantes = (lista.nueva_fecha - fecha_actual).days
        return context


class ListasEnviarView(View):

    def post(self, request, lista_id):
        try:
            lista = ListaEnviar.objects.get(id=lista_id)
            grupos = ['SUPERVISOR','GERENTE_SUCURSAL']  # Lista de nombres de grupos a verificar
            pertenece_a_admin_sucursal = any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) and self.request.user.perfil.sucursal == lista.preparada.aprobada.licitacion.sucursal 
            if self.request.user.is_authenticated and (pertenece_a_admin_sucursal or self.request.user == lista.preparada.aprobada.licitacion.user or self.request.user.groups.filter(name='GERENTE_GENERAL').exists()):
                lista.terminado = True
                lista.save()
                Enviada.objects.create(listaenviar=lista).save()
                return JsonResponse({'success': True})
        except ListaEnviar.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'La lista no existe.'})

    
class ListaEnviarDetailView(DetailView):
    model = ListaEnviar
    template_name = 'pages/listasenviar/detalle_listaenviar.html'
    context_object_name = 'listaenviar'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Detalle Listas para Enviar"
        context["card_title"] = f"Siniestro - {self.object.preparada.aprobada.licitacion.numero_siniestro}"
        context["list_url"] = reverse_lazy('seguros:listar_listasenviar')
        return context


class EnviadaListView(ListView):
    model = Enviada
    queryset = Enviada.objects.filter(activo=True, terminado=False, listaenviar__terminado=True, listaenviar__activo=True)
    context_object_name = 'enviadas'
    template_name = 'pages/enviadas/listar_enviadas.html'
    ordering = ('-creado',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Enviadas"
        context["card_title"] = "Licitaciones enviadas"
        context["list_url"] = reverse_lazy('seguros:listar_enviadas')
        return context


class EnviadaDetailView(DetailView):
    model = Enviada
    template_name = 'pages/enviadas/detalle_enviada.html'
    context_object_name = 'enviada'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Detalle Enviada"
        context["card_title"] = f"Siniestro - {self.object.listaenviar.preparada.aprobada.licitacion.numero_siniestro}"
        context["list_url"] = reverse_lazy('seguros:listar_enviadas')
        return context


class EnviadaUpdateView(UserPassesTestMixin, UpdateView):
    model = Enviada
    form_class = EnviadaForm
    template_name = 'pages/enviadas/editar_enviada.html'
    success_url = reverse_lazy('seguros:listar_enviadas')

    def test_func(self):
        grupos = ['SUPERVISOR','GERENTE_SUCURSAL']  # Lista de nombres de grupos a verificar
        pertenece_a_admin_sucursal = any(self.request.user.groups.filter(name=grupo).exists() for grupo in grupos) and self.request.user.perfil.sucursal == self.get_object().listaenviar.preparada.aprobada.licitacion.sucursal 
        return self.request.user.is_authenticated and (pertenece_a_admin_sucursal or self.request.user == self.get_object().listaenviar.preparada.aprobada.licitacion.user or self.request.user.groups.filter(name='GERENTE_GENERAL').exists())

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            accion = request.POST['accion']
            if accion == 'editar':
                form = self.get_form()
                if form.is_valid():
                    data = form.save()
                else:
                    # En el caso de errores, incluir detalles en el diccionario 'data'
                    data['error'] = 'NO se guardó la licitación'
                    data['form_errors'] = form.errors
            else:
                data['error'] = 'NO ha ingresado una acción válida'

            # Verificar si ambos campos factura y remito están cargados
            if 'factura' in request.POST and 'remito' in request.POST:
                self.object.terminado = True
                self.object.save()
                
        except forms.ValidationError as e:
            data['error'] = str(e)
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Enviada"
        context["card_title"] = f"Editar Siniestro - { self.get_object().listaenviar.preparada.aprobada.licitacion.numero_siniestro}"
        context["accion"] = "editar"
        context["list_url"] = reverse_lazy('seguros:listar_enviadas')
        return context


class TerminadaListView(ListView):
    model = Enviada
    queryset = Enviada.objects.filter(activo=True, terminado=True, listaenviar__terminado=True, listaenviar__activo=True)
    context_object_name = 'terminadas'
    template_name = 'pages/terminadas/listar_terminadas.html'
    ordering = ('-creado',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Terminadas"
        context["card_title"] = "Licitaciones terminadas"
        context["list_url"] = reverse_lazy('seguros:listar_terminadas')
        return context


class TerminadaDetailView(DetailView):
    model = Enviada
    template_name = 'pages/terminadas/detalle_terminada.html'
    context_object_name = 'enviada'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_page"] = "Detalle terminada"
        context["card_title"] = f"Siniestro - {self.object.listaenviar.preparada.aprobada.licitacion.numero_siniestro}"
        context["list_url"] = reverse_lazy('seguros:listar_terminadas')
        return context


class ObtenerPeritosView(ListView):
    model = Perito
    template_name = 'detalle.html'

    def get_queryset(self):
        aseguradora_id = self.kwargs.get('aseguradora_id')
        return Perito.objects.filter(aseguradora_id=aseguradora_id)

    def render_to_response(self, context, **response_kwargs):
        # Generar opciones para el select
        options = '<option value="">---------</option>'
        for perito in context['perito_list']:
            options += f'<option value="{perito.id}">{perito.nombre}</option>'

        return JsonResponse({'options': options})
