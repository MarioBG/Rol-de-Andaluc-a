# Generated by Django 3.2.18 on 2023-11-21 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0061_auto_20231101_0054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mapgeometry',
            name='geometry',
        ),
        migrations.RemoveField(
            model_name='mappoint',
            name='point',
        ),
    ]