# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-22 21:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matchday', '0015_auto_20170822_2106'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='highlightsUrl',
        ),
    ]
