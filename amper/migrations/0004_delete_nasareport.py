# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-29 09:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amper', '0003_report_completed'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NasaReport',
        ),
    ]
