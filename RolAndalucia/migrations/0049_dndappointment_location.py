# Generated by Django 2.2.24 on 2021-10-27 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0048_auto_20211027_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='dndappointment',
            name='location',
            field=models.CharField(max_length=72, null=True, verbose_name='Ubicación'),
        ),
    ]
