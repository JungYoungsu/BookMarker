# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-26 10:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0004_auto_20161126_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seatgroup',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='location.Location'),
        ),
    ]
