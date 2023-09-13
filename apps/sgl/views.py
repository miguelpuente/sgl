from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from .models import Licitacion
from .form import ContestadoForm, AprobadoForm, PreparadoForm, ListoForm, EnviadoForm


class Inicio(TemplateView):
    '''Inicio de la aplicación SGL'''
    template_name = 'index.html'


class ContestadoCreateView(CreateView):
    model = Licitacion
    form_class = ContestadoForm
    template_name = 'sgl/contestado/crear_contestado.html'
    success_url = reverse_lazy('listar_contestado')

    def form_valid(self, form):
        if form.instance.aprobado:
            form.instance.estado = 'APRO'
        return super().form_valid(form)


class ContestadoListView(View):
    model = Licitacion
    form_class = ContestadoForm
    template_name = 'sgl/contestado/listar_contestado.html'

    def get_queryset(self):
        return self.model.objects.filter(estado='CONT', activo=True)

    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['contestados'] = self.get_queryset()
        contexto['form'] = self.form_class
        return contexto

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ContestadoUpdateView(UpdateView):
    model = Licitacion
    template_name = 'sgl/contestado/contestado.html'
    form_class = ContestadoForm
    context_object_name = 'contestados'
    queryset = Licitacion.objects.filter(estado='CONT', activo=True)
    success_url = reverse_lazy('listar_contestado')

    def form_valid(self, form):
        if form.instance.aprobado:
            form.instance.estado = 'APRO'
        return super().form_valid(form)


class ContestadoDeleteView(DeleteView):
    model = Licitacion

    def post(self, request, pk, *args, **kwargs):
        object = Licitacion.objects.filter(id=pk)
        if object:
            object = Licitacion.objects.get(id=pk)
            object.activo = False
            object.save()

        return redirect('listar_contestado')


class AprobadoListView(ListView):
    model = Licitacion
    template_name = 'sgl/aprobado/listar_aprobado.html'
    context_object_name = 'aprobados'
    queryset = Licitacion.objects.filter(estado='APRO', activo=True)


class AprobadoUpdateView(UpdateView):
    model = Licitacion
    template_name = 'sgl/aprobado/aprobado.html'
    form_class = AprobadoForm
    context_object_name = 'aprobados'
    success_url = reverse_lazy('listar_aprobado')

    def form_valid(self, form):
        if form.instance.aprobado:
            form.instance.estado = 'APRO'
        else:
            form.instance.estado = 'CONT'
            form.instance.fecha_aprobado = None
            form.instance.numero_orden_compra = None
            form.instance.fecha_entrega_pactada = None

        if form.instance.fecha_aprobado:
            if form.instance.dias_demora == 'SINDI':
                days_to_add = 0
            elif form.instance.dias_demora == 'INMED':
                days_to_add = 1
            elif form.instance.dias_demora == '01-01':
                days_to_add = 1
            elif form.instance.dias_demora == '02-02':
                days_to_add = 2
            elif form.instance.dias_demora == '03-03':
                days_to_add = 3
            elif form.instance.dias_demora == '04-07':
                days_to_add = 7
            elif form.instance.dias_demora == '07-15':
                days_to_add = 15
            elif form.instance.dias_demora == '15-30':
                days_to_add = 30
            elif form.instance.dias_demora == '30-30':
                days_to_add = 60

            form.instance.fecha_entrega_pactada = form.instance.fecha_aprobado + \
                timedelta(days=days_to_add)
            form.instance.estado = 'PREP'
            form.instance.fecha_preparacion = datetime.now()

        return super().form_valid(form)


class AprobadoDeleteView(DeleteView):
    model = Licitacion

    def post(self, request, pk, *args, **kwargs):
        object = Licitacion.objects.filter(id=pk)
        if object:
            object = Licitacion.objects.get(id=pk)
            object.activo = False
            object.save()

        return redirect('listar_aprobado')


class PreparadoListView(ListView):
    model = Licitacion
    template_name = 'sgl/preparado/listar_preparado.html'
    context_object_name = 'preparados'
    queryset = Licitacion.objects.filter(estado='PREP', activo=True)


class PreparadoUpdateView(UpdateView):
    model = Licitacion
    template_name = 'sgl/preparado/preparado.html'
    form_class = PreparadoForm
    context_object_name = 'preparados'
    success_url = reverse_lazy('listar_preparado')

    def form_valid(self, form):
        if form.instance.preparado:
            form.instance.estado = 'LIST'
            form.instance.fecha_listo_enviar = datetime.now()
        else:
            form.instance.estado = 'PREP'

        return super().form_valid(form)


class PreparadoDeleteView(DeleteView):
    model = Licitacion

    def post(self, request, pk, *args, **kwargs):
        object = Licitacion.objects.filter(id=pk)
        if object:
            object = Licitacion.objects.get(id=pk)
            object.activo = False
            object.save()

        return redirect('listar_preparado')


class ListoEnviarListView(ListView):
    model = Licitacion
    template_name = 'sgl/listo_enviar/listar_listo_enviar.html'
    context_object_name = 'listos'
    queryset = Licitacion.objects.filter(estado='LIST', activo=True)


class ListoEnviarUpdateView(UpdateView):
    model = Licitacion
    template_name = 'sgl/listo_enviar/listo.html'
    form_class = ListoForm
    context_object_name = 'listos'
    success_url = reverse_lazy('listar_listo_enviar')

    def form_valid(self, form):
        if form.instance.enviado:
            form.instance.estado = 'ENVI'
            form.instance.fecha_enviado = datetime.now()
        else:
            form.instance.estado = 'LIST'

        return super().form_valid(form)


class ListoEnviarDeleteView(DeleteView):
    model = Licitacion

    def post(self, request, pk, *args, **kwargs):
        object = Licitacion.objects.filter(id=pk)
        if object:
            object = Licitacion.objects.get(id=pk)
            object.activo = False
            object.save()

        return redirect('listar_listo_enviar')


class EnviadoListView(ListView):
    model = Licitacion
    template_name = 'sgl/enviado/listar_enviado.html'
    context_object_name = 'listos'
    queryset = Licitacion.objects.filter(estado='ENVI', activo=True)


class EnviadoUpdateView(UpdateView):
    model = Licitacion
    template_name = 'sgl/enviado/enviado.html'
    form_class = EnviadoForm
    context_object_name = 'enviados'
    success_url = reverse_lazy('listar_enviado')

    def form_valid(self, form):
        if not form.instance.enviado:
            form.instance.fecha_enviado = None
            form.instance.estado = 'LIST'
            form.instance.transporte = None
            form.instance.factura = None
            form.instance.remito = None
            form.instance.comentarios_envio = None
        return super().form_valid(form)
