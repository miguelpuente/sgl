import uuid
from django.contrib.auth.models import User
from apps.empresa.models import Sucursal
from django.db import models


class Perfil(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    imagen = models.ImageField(
        upload_to='users/imagenes',
        blank=True,
        null=True
    )
    modificado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['user']

    def __str__(self):
        return self.user.username
