# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-08 14:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('matchday', '0004_matchstatus_sortorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='matchday.Match'),
        ),
    ]
