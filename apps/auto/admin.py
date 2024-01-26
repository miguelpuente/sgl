from django.contrib import admin
from .models import Marca, Modelo

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('nombre',)