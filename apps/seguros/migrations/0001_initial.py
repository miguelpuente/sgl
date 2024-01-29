# Generated by Django 4.2.7 on 2024-01-28 01:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('empresa', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auto', '__first__'),
        ('direccion', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aprobada',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fecha_aprobado', models.DateField(blank=True, null=True)),
                ('numero_orden_compra', models.PositiveIntegerField(blank=True, null=True)),
                ('numero_nota_pedido', models.PositiveIntegerField(blank=True, null=True)),
                ('terminado', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Aprobada',
                'verbose_name_plural': 'Aprobadas',
                'ordering': ['creado'],
            },
        ),
        migrations.CreateModel(
            name='Aseguradora',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=150, null=True)),
                ('telefono', models.CharField(blank=True, max_length=250, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Aseguradora',
                'verbose_name_plural': 'Aseguradoras',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Demora',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('dia', models.PositiveIntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Demora',
                'verbose_name_plural': 'Demoras',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Taller',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=150, null=True)),
                ('telefono', models.CharField(blank=True, max_length=250, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Taller',
                'verbose_name_plural': 'Talleres',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Transporte',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(blank=True, max_length=150, null=True)),
                ('telefono', models.CharField(blank=True, max_length=250, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Transporte',
                'verbose_name_plural': 'Transportes',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Preparada',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('cantidad_articulos_listos', models.IntegerField(blank=True, null=True)),
                ('terminado', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateField(auto_now_add=True)),
                ('aprobada', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguros.aprobada')),
            ],
            options={
                'verbose_name': 'Preparada',
                'verbose_name_plural': 'Preparadas',
                'ordering': ['creado'],
            },
        ),
        migrations.CreateModel(
            name='Perito',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=150, null=True)),
                ('telefono', models.CharField(blank=True, max_length=250, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('aseguradora', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguros.aseguradora')),
            ],
            options={
                'verbose_name': 'Perito',
                'verbose_name_plural': 'Peritos',
                'ordering': ['aseguradora'],
            },
        ),
        migrations.CreateModel(
            name='ListaEnviar',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('terminado', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateField(auto_now_add=True)),
                ('preparada', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguros.preparada')),
            ],
            options={
                'verbose_name': 'Lista para enviar',
                'verbose_name_plural': 'Listas para enviar',
                'ordering': ['creado'],
            },
        ),
        migrations.CreateModel(
            name='Licitacion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('numero_siniestro', models.PositiveIntegerField(unique=True)),
                ('dominio', models.CharField(max_length=7)),
                ('numero_presupuesto', models.PositiveIntegerField(unique=True)),
                ('cantidad_articulos', models.PositiveIntegerField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('costo_transporte', models.DecimalField(decimal_places=2, max_digits=10)),
                ('terminado', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateTimeField(auto_now_add=True)),
                ('aseguradora', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguros.aseguradora')),
                ('datos_entrega', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='direccion.datoentrega')),
                ('demora', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguros.demora')),
                ('perito', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='seguros.perito')),
                ('sucursal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='empresa.sucursal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auto.modelo')),
            ],
            options={
                'verbose_name': 'Licitacion',
                'verbose_name_plural': 'Licitaciones',
                'ordering': ['creado'],
            },
        ),
        migrations.CreateModel(
            name='Enviada',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('factura', models.CharField(blank=True, max_length=15, null=True)),
                ('remito', models.ImageField(blank=True, null=True, upload_to='remitos/')),
                ('terminado', models.BooleanField(default=False)),
                ('activo', models.BooleanField(default=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('creado', models.DateField(auto_now_add=True)),
                ('listaenviar', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguros.listaenviar')),
            ],
            options={
                'verbose_name': 'Enviada',
                'verbose_name_plural': 'Enviadas',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='aprobada',
            name='licitacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='seguros.licitacion'),
        ),
        migrations.AddField(
            model_name='aprobada',
            name='taller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='seguros.taller'),
        ),
        migrations.AddField(
            model_name='aprobada',
            name='transporte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='seguros.transporte'),
        ),
    ]
