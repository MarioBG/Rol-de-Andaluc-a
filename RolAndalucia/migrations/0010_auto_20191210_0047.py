# Generated by Django 2.2.4 on 2019-12-09 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0009_auto_20191210_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personaje',
            name='hechizos',
            field=models.ManyToManyField(blank=True, to='RolAndalucia.Spell', verbose_name='Hechizos'),
        ),
    ]