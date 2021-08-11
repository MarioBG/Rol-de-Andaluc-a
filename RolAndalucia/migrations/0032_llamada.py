# Generated by Django 2.2 on 2021-08-10 21:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0031_nota'),
    ]

    operations = [
        migrations.CreateModel(
            name='Llamada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=32, verbose_name='Numero')),
                ('hora', models.CharField(max_length=32, verbose_name='Hora')),
                ('tipo', models.CharField(choices=[('REC', 'Recibida'), ('ENV', 'Enviada'), ('PER', 'Perdida')], max_length=8, verbose_name='Hora')),
                ('movil', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='llamadas', to='RolAndalucia.Movil')),
            ],
        ),
    ]
