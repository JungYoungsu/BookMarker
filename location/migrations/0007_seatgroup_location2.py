# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-26 14:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0006_auto_20161126_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='seatgroup',
            name='location2',
            field=models.IntegerField(default=0),
        ),
    ]