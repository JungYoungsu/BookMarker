# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-17 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0005_bookshelf_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookshelf',
            name='number',
        ),
        migrations.AddField(
            model_name='bookshelf',
            name='name',
            field=models.CharField(default=None, max_length=64),
        ),
    ]
