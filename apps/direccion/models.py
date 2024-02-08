import uuid
from django.db import models

class Provincia(models.Model):
    id = models.IntegerField(primary_key=True)
    provincia = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['provincia']

    def __str__(self):
        return f'{self.provincia}'


class Localidad(models.Model):
    id = models.IntegerField(primary_key=True)
    localidad = models.CharField(max_length=255)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        ordering = ['localidad']

    def __str__(self):
        return f'{self.localidad}'


class DatoEntrega(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direccion = models.CharField(max_length=250, null=True, blank=True)
    localidad = models.ForeignKey(
        Localidad, on_delete=models.PROTECT, null=True, blank=True)
    nombre_persona_recibe = models.CharField(max_length=250, null=True, blank=True)
    telefono_persona_recibe = models.CharField(max_length=250, null=True, blank=True)
    creado = models.DateField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'DatoEntrega'
        verbose_name_plural = 'DatoEntregas'
        ordering = ['direccion']

    def __str__(self):
        return f'{self.direccion}'