from django.contrib import admin
from .models import Licitacion, Aprobada, Preparada, ListaEnviar, Enviada, Aseguradora, Perito, Transporte, Taller, Demora

@admin.register(Licitacion)
class LicitacionAdmin(admin.ModelAdmin):
    list_display = ('numero_siniestro', 'user', 'sucursal', 'aseguradora', 'perito', 'demora', 'vehiculo', 'dominio', 'numero_presupuesto')
    list_filter = ('user', 'sucursal', 'aseguradora', 'vehiculo')
    list_editable = ('user', 'sucursal')

@admin.register(Aprobada)
class AprobadaAdmin(admin.ModelAdmin):
    list_display = ('licitacion',)

@admin.register(Transporte)
class TransporteAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Aseguradora)
class AseguradoraAdmin(admin.ModelAdmin):
    list_display = ('nombre',)


@admin.register(Demora)
class DemoraAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Perito)
class PeritoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)