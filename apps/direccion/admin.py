from django.contrib import admin
from .models import Provincia, Localidad

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ('provincia',)

@admin.register(Localidad)
class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('localidad',)