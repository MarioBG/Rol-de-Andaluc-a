# Generated by Django 3.2.18 on 2023-04-01 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0059_wikiarticle_redirect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikiarticle',
            name='redirect',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
