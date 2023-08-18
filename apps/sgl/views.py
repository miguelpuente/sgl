from django.views.generic import TemplateView


class ContestadoView(TemplateView):
    template_name = 'contestado/contestados.html'


class AprobadoView(TemplateView):
    template_name = 'aprobado/aprobados.html'


class PreparacionView(TemplateView):
    template_name = 'preparado/preparado.html'


class ListoEnviarView(TemplateView):
    template_name = 'listo_enviar/listo_enviar.html'
