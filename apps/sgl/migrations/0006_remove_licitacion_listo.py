# Generated by Django 4.2.2 on 2023-09-11 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sgl', '0005_licitacion_listo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='licitacion',
            name='listo',
        ),
    ]