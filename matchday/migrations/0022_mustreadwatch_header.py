# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-07 08:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchday', '0021_auto_20171007_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='mustreadwatch',
            name='header',
            field=models.CharField(default='MUST READ', max_length=15),
            preserve_default=False,
        ),
    ]
