from django.contrib import admin
from . import models

admin.site.register(models.Aseguradora)
admin.site.register(models.DatoEntrega)
admin.site.register(models.Perito)

class ProvinciaAdmin(admin.ModelAdmin):
    search_fields = ('provincia'),
    ordering = ['provincia']

admin.site.register(models.Provincia, ProvinciaAdmin)


class LocalidadAdmin(admin.ModelAdmin):
    ordering = ['localidad']
    search_fields = ('localidad'),
    autocomplete_fields = ['provincia']

admin.site.register(models.Localidad, LocalidadAdmin)

class LicitacionAdmin(admin.ModelAdmin):
    ordering = ['fecha_contestado']
    autocomplete_fields = ['localidad']

admin.site.register(models.Licitacion, LicitacionAdmin)

admin.site.register(models.Transporte)
