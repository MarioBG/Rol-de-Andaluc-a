# Generated by Django 3.2.18 on 2025-01-15 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RolAndalucia', '0067_answer_poll_pollparticipation_question_voter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='title',
            field=models.CharField(default='Lorem ipsum dolor sit amet', max_length=120, verbose_name='Texto'),
        ),
    ]
