# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-20 05:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlshortenerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='text',
            field=models.CharField(max_length=50000000),
        ),
    ]