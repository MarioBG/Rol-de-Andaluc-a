# Generated by Django 3.2.18 on 2023-03-26 17:42

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0054_auto_20211229_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('body', martor.models.MartorField(blank=True, default='', verbose_name='Habilidades')),
                ('points', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
                ('geometries', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
