# Generated by Django 4.2.2 on 2023-09-15 15:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aseguradora',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('telefono', models.CharField(max_length=250)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Aseguradora',
                'verbose_name_plural': 'Aseguradoras',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='DatoEntrega',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('direccion', models.CharField(max_length=250)),
                ('nombre_persona_recibe', models.CharField(max_length=250)),
                ('telefono_persona_recibe', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'DatoEntrega',
                'verbose_name_plural': 'DatoEntregas',
                'ordering': ['direccion'],
            },
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('provincia', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
                'ordering': ['provincia'],
            },
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('telefono', models.CharField(max_length=250)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Transporte',
                'verbose_name_plural': 'Transportes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Perito',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=150)),
                ('telefono', models.CharField(max_length=250)),
                ('activo', models.BooleanField(default=True)),
                ('aseguradora', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgl.aseguradora')),
            ],
            options={
                'verbose_name': 'Perito',
                'verbose_name_plural': 'Peritos',
                'ordering': ['aseguradora'],
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.IntegerField(editable=False, primary_key=True, serialize=False)),
                ('localidad', models.CharField(max_length=60)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sgl.provincia')),
            ],
            options={
                'verbose_name': 'Localidad',
                'verbose_name_plural': 'Localidades',
                'ordering': ['localidad'],
            },
        ),
        migrations.CreateModel(
            name='Licitacion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('sucursal', models.CharField(blank=True, choices=[('CH', 'Charata'), ('SP', 'Sáenz Peña'), ('RE', 'Resistencia')], max_length=5, null=True)),
                ('dias_demora', models.CharField(blank=True, choices=[('SINDI', 'Sin Disponibilidad'), ('INMED', 'Inmediata'), ('01-01', '1 día'), ('02-02', '2 días'), ('03-03', '3 días'), ('04-07', 'Entre 4 y 7 días'), ('07-15', 'Entre 7 y 15 días'), ('15-30', 'Entre 15 y 30 días'), ('30-30', 'Más de 30 días')], default='06-10', max_length=5, null=True)),
                ('vehiculo', models.CharField(blank=True, choices=[('COR', 'COROLLA'), ('YAR', 'YARIS'), ('ETI', 'ETIOS'), ('SW4', 'SW4'), ('HIL', 'HILUX'), ('CHR', 'CHR'), ('RAV', 'RAV4'), ('CCR', 'COROLLA CROSS'), ('CAM', 'CAMRY'), ('HIA', 'HIACE')], default='HIL', max_length=3, null=True)),
                ('estado', models.CharField(blank=True, choices=[('CONT', 'Contestado'), ('APRO', 'Aprobado'), ('PREP', 'En Preparación'), ('LIST', 'Listo para enviar'), ('ENVI', 'Enviado')], default='CONT', max_length=4, null=True)),
                ('fecha_contestado', models.DateField(blank=True, null=True)),
                ('fecha_aprobado', models.DateField(blank=True, null=True)),
                ('fecha_preparacion', models.DateField(blank=True, null=True)),
                ('fecha_entrega_pactada', models.DateField(blank=True, null=True)),
                ('fecha_listo_enviar', models.DateField(blank=True, null=True)),
                ('fecha_enviado', models.DateField(blank=True, null=True)),
                ('comentarios_preparacion', models.TextField(blank=True, null=True)),
                ('comentarios_listo_enviar', models.TextField(blank=True, null=True)),
                ('comentarios_envio', models.TextField(blank=True, null=True)),
                ('dominio', models.CharField(blank=True, max_length=7, null=True)),
                ('numero_presupuesto', models.BigIntegerField(blank=True, null=True)),
                ('numero_siniestro', models.BigIntegerField(unique=True)),
                ('numero_orden_compra', models.BigIntegerField(blank=True, null=True)),
                ('numero_nota_pedido', models.BigIntegerField(blank=True, null=True)),
                ('cantidad_articulos', models.IntegerField(blank=True, null=True)),
                ('factura', models.CharField(blank=True, max_length=15, null=True)),
                ('monto', models.FloatField(blank=True, null=True)),
                ('costo_transporte', models.FloatField(blank=True, null=True)),
                ('remito', models.ImageField(blank=True, null=True, upload_to='remitos/')),
                ('enviado', models.BooleanField(default=False)),
                ('preparado', models.BooleanField(default=False)),
                ('aprobado', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('create_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('aseguradora', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sgl.aseguradora')),
                ('datos_entrega', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sgl.datoentrega')),
                ('localidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sgl.localidad')),
                ('perito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sgl.perito')),
                ('provincia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sgl.provincia')),
                ('transporte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sgl.transporte')),
            ],
            options={
                'verbose_name': 'Licitacion',
                'verbose_name_plural': 'Licitaciones',
                'ordering': ['numero_siniestro'],
            },
        ),
    ]
