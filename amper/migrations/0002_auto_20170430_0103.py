# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-29 23:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capacityhour',
            name='hour',
            field=models.DateTimeField(unique=True),
        ),
    ]
