# Generated by Django 2.2.24 on 2021-10-26 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0044_auto_20211024_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='dndrsvp',
            name='type',
            field=models.CharField(choices=[('YES', 'Quiero este horario'), ('IF_NEED', 'Solo si es necesario')], default='YES', max_length=30, verbose_name='Tipo de reserva'),
            preserve_default=False,
        ),
    ]
