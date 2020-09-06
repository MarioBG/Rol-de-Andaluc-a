# Generated by Django 3.1 on 2020-08-15 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0025_auto_20200813_2042'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ability',
            name='habilidadPadre',
        ),
        migrations.AddField(
            model_name='ability',
            name='expCost',
            field=models.IntegerField(default=0, verbose_name='Coste en experiencia'),
        ),
        migrations.AddField(
            model_name='ability',
            name='isOptional',
            field=models.BooleanField(default=False, verbose_name='Habilidad opcional'),
        ),
    ]
