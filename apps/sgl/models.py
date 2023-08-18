import uuid
from django.db import models

class Aseguradora(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=250)
    activo = models.BooleanField(default=True)

class Perito(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=250)
    activo = models.BooleanField(default=True)

class Provincia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)

class Localidad(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)

class DatoEntrega(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    direccion = models.CharField(max_length=250)
    nombre_persona_recibe = models.CharField(max_length=250)
    telefono_persona_recibe = models.CharField(max_length=250)

class Transporte(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    telefono = models.CharField(max_length=250)
    activo = models.BooleanField(default=True)

dias_demora_choices = (
    ('01-05', 'de 1 a 5 días'),
    ('06-10', 'de 6 a 10 días'),
    ('11-15', 'de 11 a 15 días'),
    ('16-20', 'de 16 a 20 días'),
)

modelos_vehiculo_choices = (
    ('HIL', 'Hilux'),
    ('YAR', 'Yaris'),
    ('ETI', 'Etios'),
    ('SW4', 'SW4'),
    ('COR', 'Corolla'),
    ('PRI', 'Prius'),
    ('INN', 'Innova'),
)

sucursales_choices = (
    ('CH', 'Charata'),
    ('SP', 'Sáenz Peña'),
    ('RE', 'Resistencia'),
)

estados_choices = (
    ('CONT', 'Contestado'),
    ('APRO', 'Aprobado'),
    ('PREP', 'En Preparación'),
    ('LIST', 'Listo para enviar'),
    ('ENVI', 'Enviado'),
)

class Licitacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_sucursal = models.CharField(
        max_length=5,
        choices = sucursales_choices,
        null=True,
        blank=True,
    )
    # usuario
    id_aseguradora = models.ForeignKey(Aseguradora, on_delete=models.CASCADE, null=True, blank=True)
    id_perito = models.ForeignKey(Perito, on_delete=models.CASCADE, null=True, blank=True)
    dias_demora = models.CharField(
        max_length=5,
        choices = dias_demora_choices,
        default = '06-10',
        null=True,
        blank=True,
    )
    vehiculo = models.CharField(
        max_length=3,
        choices = modelos_vehiculo_choices,
        default = 'HIL',
    null=True,
    blank=True
    )
    id_localidad = models.ForeignKey(Localidad, on_delete=models.CASCADE, null=True, blank=True)
    id_datos_entrega = models.ForeignKey(DatoEntrega, on_delete=models.CASCADE, null=True, blank=True)
    estado = models.CharField(
        max_length=4,
        choices = estados_choices,
        default = 'CONT',
        null=True,
        blank=True
    )
    id_transporte = models.ForeignKey(Transporte, on_delete=models.CASCADE, null=True, blank=True)
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
    numero_presupuesto = models.IntegerField(null=True, blank=True)
    numero_siniestro = models.IntegerField(null=True, blank=True)
    numero_orden_compra = models.IntegerField(null=True, blank=True)
    numero_nota_pedido = models.IntegerField(null=True, blank=True)
    cantidad_articulos = models.IntegerField(null=True, blank=True)
    factura = models.CharField(max_length=15, null=True, blank=True)
    monto = models.FloatField(null=True, blank=True)
    costo_transporte = models.FloatField(null=True, blank=True)
    remito = models.ImageField(upload_to='remitos/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)