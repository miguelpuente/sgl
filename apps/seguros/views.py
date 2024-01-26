from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView, ListView, UpdateView, DeleteView
from .models import Licitacion, Aprobada, Preparada, ListaEnviar, Enviada, Perito
from .forms import LicitacioForm
from apps.direccion.models import DatoEntrega, Provincia, Localidad

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
    #         if accion == 'buscardata':
    #             data = []
    #             for licitacion in Licitacion.objects.filter(activo=True, terminado=False):
    #                 data.append(licitacion.toJSON())
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
    form_class = LicitacioForm
    template_name = 'pages/licitaciones/crear_licitacion.html'
    success_url = reverse_lazy('seguros:listar_licitaciones')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['accion']
            if action == 'agregar':
                form = self.get_form()
                if form.is_valid():
                    form.instance.datos_entrega = DatoEntrega.objects.create(localidad=form.cleaned_data['localidad'])
                    data = form.save()
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


class LicitacionUpdateView(UpdateView):
    model = Licitacion
    form_class = LicitacioForm
    template_name = 'pages/licitaciones/crear_licitacion.html'
    success_url = reverse_lazy('seguros:listar_licitaciones')

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
                    localidad = DatoEntrega.objects.get(id = form.instance.datos_entrega_id)
                    localidad.localidad = form.cleaned_data['localidad']
                    localidad.save()
                    Aprobada.objects.create(licitacion=form.instance).save()
                    data = form.save()
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


class LicitacionDeleteView(DeleteView):
    model = Licitacion
    template_name = 'pages/licitaciones/eliminar_licitacion.html'
    success_url = reverse_lazy('seguros:listar_licitaciones')

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

    
# class BuscarListView(ListView):
#     template_name = 'operaciones.html'
#     model = Licitacion
#     context_object_name = 'licitaciones'

#     def get_queryset(self):
#         termino_busqueda = self.request.GET.get('termino_busqueda', '')
#         print(termino_busqueda)
#         licitaciones = Licitacion.objects.filter(activo=True)
#         if termino_busqueda:
#             licitaciones = Licitacion.objects.filter(
#                 Q(localidad__localidad__icontains=termino_busqueda) |
#                 Q(localidad__provincia__provincia__icontains=termino_busqueda) |
#                 Q(dominio__icontains=termino_busqueda) |
#                 Q(numero_siniestro__icontains=termino_busqueda) |
#                 Q(transporte__nombre__icontains=termino_busqueda)
#                 # Agrega más condiciones según sea necesario
#             )
#             print(licitaciones)
#         return licitaciones

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['operacion'] = 'Contestados'
#         return context





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
