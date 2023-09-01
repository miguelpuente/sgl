import uuid
from django.db import models
from .choices import dias_demora, estados, modelos_vehiculo, sucursales


class Aseguradora(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=250)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Aseguradora'
        verbose_name_plural = 'Aseguradoras'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Perito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=250)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Perito'
        verbose_name_plural = 'Peritos'
        ordering = ['aseguradora']

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    provincia = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['provincia']

    def __str__(self):
        return self.provincia


class Localidad(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    localidad = models.CharField(max_length=60)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Localidad'
        verbose_name_plural = 'Localidades'
        ordering = ['localidad']

    def __str__(self):
        return self.localidad


class DatoEntrega(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direccion = models.CharField(max_length=250)
    nombre_persona_recibe = models.CharField(max_length=250)
    telefono_persona_recibe = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'DatoEntrega'
        verbose_name_plural = 'DatoEntregas'
        ordering = ['direccion']

    def __str__(self):
        return self.direccion


class Transporte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=250)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Transporte'
        verbose_name_plural = 'Transportes'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Licitacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sucursal = models.CharField(
        max_length=5,
        choices=sucursales,
        null=True,
        blank=True,
    )
    # usuario
    aseguradora = models.ForeignKey(
        Aseguradora, on_delete=models.CASCADE, null=True, blank=True)
    perito = models.ForeignKey(
        Perito, on_delete=models.CASCADE, null=True, blank=True)
    dias_demora = models.CharField(
        max_length=5,
        choices=dias_demora,
        default='06-10',
        null=True,
        blank=True,
    )
    vehiculo = models.CharField(
        max_length=3,
        choices=modelos_vehiculo,
        default='HIL',
        null=True,
        blank=True
    )
    localidad = models.ForeignKey(
        Localidad, on_delete=models.CASCADE, null=True, blank=True)
    datos_entrega = models.ForeignKey(
        DatoEntrega, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(
        max_length=4,
        choices=estados,
        default='CONT',
        null=True,
        blank=True
    )
    transporte = models.ForeignKey(
        Transporte, on_delete=models.CASCADE, null=True, blank=True)
    fecha_contestado = models.DateField(null=True, blank=True)
    fecha_aprobado = models.DateField(null=True, blank=True)
    fecha_preparacion = models.DateField(null=True, blank=True)
    fecha_entrega_pactada = models.DateField(null=True, blank=True)
    fecha_listo_enviar = models.DateField(null=True, blank=True)
    fecha_enviado = models.DateField(null=True, blank=True)
    comentarios_preparacion = models.TextField(null=True, blank=True)
    comentarios_listo_enviar = models.TextField(null=True, blank=True)
    comentarios_envio = models.TextField(null=True, blank=True)
    dominio = models.CharField(max_length=7, null=True, blank=True)
    numero_presupuesto = models.BigIntegerField(null=True, blank=True)
    numero_siniestro = models.BigIntegerField(null=True, blank=True)
    numero_orden_compra = models.BigIntegerField(null=True, blank=True)
    numero_nota_pedido = models.BigIntegerField(null=True, blank=True)
    cantidad_articulos = models.IntegerField(null=True, blank=True)
    factura = models.CharField(max_length=15, null=True, blank=True)
    monto = models.FloatField(null=True, blank=True)
    costo_transporte = models.FloatField(null=True, blank=True)
    remito = models.ImageField(upload_to='remitos/', null=True, blank=True)
    aprobado = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Licitacion'
        verbose_name_plural = 'Licitaciones'
        ordering = ['numero_siniestro']

    def __str__(self):
        return str(self.numero_siniestro)
