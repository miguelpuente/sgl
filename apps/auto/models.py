import uuid
from django.db import models

class Marca(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre}'

class Modelo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Modelo'
        verbose_name_plural = 'modelos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre}'