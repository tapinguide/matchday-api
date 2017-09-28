# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-14 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchday', '0007_auto_20170408_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortCode', models.CharField(max_length=5)),
                ('text', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=250)),
            ],
        ),
    ]
