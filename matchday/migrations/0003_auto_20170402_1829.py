# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-02 18:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchday', '0002_matchstatus_descriptions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='matchstatus',
            name='descriptions',
        ),
        migrations.RemoveField(
            model_name='matchstatus',
            name='sortOrder',
        ),
    ]
