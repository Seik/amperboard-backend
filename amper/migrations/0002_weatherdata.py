# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-29 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amper', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hour', models.TimeField()),
                ('humidity', models.PositiveIntegerField()),
                ('wind_speed', models.PositiveIntegerField()),
            ],
        ),
    ]
