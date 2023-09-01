from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from .models import Licitacion
from .form import ContestadoForm, AprobadoForm


class Inicio(TemplateView):
    '''Inicio de la aplicación SGL'''
    template_name = 'index.html'


class ContestadoCreateView(CreateView):
    model = Licitacion
    form_class = ContestadoForm
    template_name = 'sgl/contestado/crear_contestado.html'
    success_url = reverse_lazy('listar_contestado')


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
    success_url = reverse_lazy('listar_contestado')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contestados'] = self.model.objects.filter(
            estado='CONT', activo=True)
        return context


class ContestadoDeleteView(DeleteView):
    model = Licitacion

    def post(self, request, pk, *args, **kwargs):
        object = Licitacion.objects.filter(id=pk)
        if object:
            object = Licitacion.objects.get(id=pk)
            object.activo = False
            object.save()
            return redirect('listar_contestado')
        else:
            return redirect('listar_contestado')


class AprobadoListView(ListView):
    model = Licitacion
    template_name = 'sgl/aprobado/listar_aprobado.html'
    context_object_name = 'aprobados'
    queryset = Licitacion.objects.filter(estado='APRO', activo=True)


class AprobadoUpdateView(UpdateView):
    model = Licitacion
    template_name = 'sgl/aprobado/crear_aprobado.html'
    form_class = AprobadoForm
    context_object_name = 'aprobado_form'
    success_url = reverse_lazy('listar_aprobado')


class AprobadoDeleteView(DeleteView):
    model = Licitacion

    def post(self, request, pk, *args, **kwargs):
        object = Licitacion.objects.filter(id=pk)
        if object:
            object = Licitacion.objects.get(id=pk)
            object.activo = False
            object.save()
            return redirect('listar_aprobado')
        else:
            return redirect('listar_aprobado')


class PreparacionView(TemplateView):
    template_name = 'preparado/preparado.html'


class ListoEnviarView(TemplateView):
    template_name = 'listo_enviar/listo_enviar.html'
