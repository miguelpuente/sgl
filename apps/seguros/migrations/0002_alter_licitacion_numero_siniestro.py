# Generated by Django 4.2.7 on 2024-02-16 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seguros', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licitacion',
            name='numero_siniestro',
            field=models.CharField(max_length=20),
        ),
    ]
