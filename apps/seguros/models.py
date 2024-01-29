import uuid
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.forms import model_to_dict
from apps.empresa.models import Sucursal
from apps.auto.models import Modelo
from apps.direccion.models import DatoEntrega, Localidad
from django.db import models


class Aseguradora(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=250, null=True, blank=True)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Aseguradora'
        verbose_name_plural = 'Aseguradoras'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre.strip()

class Perito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=250, null=True, blank=True)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perito'
        verbose_name_plural = 'Peritos'
        ordering = ['aseguradora']

    def __str__(self):
        return self.nombre.strip()

class Transporte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    localidad = models.ForeignKey(
        Localidad, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=250, null=True, blank=True)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre.strip()

class Taller(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    localidad = models.ForeignKey(
        Localidad, on_delete=models.PROTECT, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    telefono = models.CharField(max_length=250, null=True, blank=True)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre.strip()

class Demora(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150, unique=True)
    dia = models.PositiveIntegerField()
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Demora'
        verbose_name_plural = 'Demoras'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre.strip()

class Licitacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    numero_siniestro = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        unique=True,
        validators=[MinValueValidator(0)],
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.PROTECT)
    perito = models.ForeignKey(Perito, on_delete=models.PROTECT, null=True, blank=True)
    demora = models.ForeignKey(Demora, on_delete=models.PROTECT)
    vehiculo = models.ForeignKey(Modelo, on_delete=models.PROTECT)
    dominio = models.CharField(max_length=7)
    numero_presupuesto = models.DecimalField(
        max_digits=20,
        decimal_places=0,
        unique=True,
        validators=[MinValueValidator(0)],
    )
    cantidad_articulos = models.DecimalField(
        max_digits=4,
        decimal_places=0,
        unique=True,
        validators=[MinValueValidator(0)],
    )
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    datos_entrega = models.ForeignKey(DatoEntrega, on_delete=models.PROTECT, null=True, blank=True)
    costo_transporte = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    terminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Licitacion'
        verbose_name_plural = 'Licitaciones'
        ordering = ['creado']

    def toJSON(self):
        return model_to_dict(self)

    def __str__(self):
        return f'{self.id}'

class Aprobada(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    licitacion = models.ForeignKey(Licitacion, on_delete=models.PROTECT)
    taller = models.ForeignKey(Taller, on_delete=models.PROTECT, null=True, blank=True)
    transporte = models.ForeignKey(Transporte, on_delete=models.PROTECT, null=True, blank=True)
    fecha_aprobado = models.DateField(null=True, blank=True)
    numero_orden_compra = models.DecimalField(
        max_digits=20, 
        decimal_places=0,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    numero_nota_pedido = models.DecimalField(
        max_digits=20, 
        decimal_places=0,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    terminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Aprobada'
        verbose_name_plural = 'Aprobadas'
        ordering = ['creado']

    def __str__(self):
        return f'{self.id}'

class Preparada(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aprobada = models.ForeignKey(Aprobada, on_delete=models.PROTECT)
    cantidad_articulos_listos = models.DecimalField(
        max_digits=4, 
        decimal_places=0,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
    )
    terminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Preparada'
        verbose_name_plural = 'Preparadas'
        ordering = ['creado']

    def __str__(self):
        return f'{self.id}'    

class ListaEnviar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    preparada = models.ForeignKey(Preparada, on_delete=models.PROTECT)
    terminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lista para enviar'
        verbose_name_plural = 'Listas para enviar'
        ordering = ['creado']

    def __str__(self):
        return f'{self.id}'

class Enviada(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    listaenviar = models.ForeignKey(ListaEnviar, on_delete=models.PROTECT)
    factura = models.CharField(max_length=15, null=True, blank=True)
    remito = models.ImageField(upload_to='remitos/', null=True, blank=True)
    terminado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    actualizado = models.DateTimeField(auto_now=True)
    creado = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Enviada'
        verbose_name_plural = 'Enviadas'
        ordering = ['id']

    def __str__(self):
        return f'{self.id}'
