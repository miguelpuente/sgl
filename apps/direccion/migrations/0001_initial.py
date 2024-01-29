# Generated by Django 4.2.7 on 2024-01-28 01:05

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('provincia', models.CharField(max_length=30)),
                ('creado', models.DateField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Provincia',
                'verbose_name_plural': 'Provincias',
                'ordering': ['provincia'],
            },
        ),
        migrations.CreateModel(
            name='Localidad',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('localidad', models.CharField(max_length=60)),
                ('creado', models.DateField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('provincia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='direccion.provincia')),
            ],
            options={
                'verbose_name': 'Localidad',
                'verbose_name_plural': 'Localidades',
                'ordering': ['localidad'],
            },
        ),
        migrations.CreateModel(
            name='DatoEntrega',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('direccion', models.CharField(blank=True, max_length=250, null=True)),
                ('nombre_persona_recibe', models.CharField(blank=True, max_length=250, null=True)),
                ('telefono_persona_recibe', models.CharField(blank=True, max_length=250, null=True)),
                ('creado', models.DateField(auto_now_add=True)),
                ('actualizado', models.DateTimeField(auto_now=True)),
                ('localidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='direccion.localidad')),
            ],
            options={
                'verbose_name': 'DatoEntrega',
                'verbose_name_plural': 'DatoEntregas',
                'ordering': ['direccion'],
            },
        ),
    ]
