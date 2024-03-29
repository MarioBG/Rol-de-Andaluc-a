# Generated by Django 3.2.18 on 2023-03-29 16:28

from django.db import migrations, models
import django.db.models.deletion
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0056_auto_20230328_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='WikiArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=512)),
                ('body', martor.models.MartorField(blank=True, default='', verbose_name='Cuerpo del artículo')),
            ],
        ),
        migrations.AlterField(
            model_name='mapgeometry',
            name='map_article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RolAndalucia.wikiarticle'),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='map_article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RolAndalucia.wikiarticle'),
        ),
        migrations.DeleteModel(
            name='MapArticle',
        ),
    ]
