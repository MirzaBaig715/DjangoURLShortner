# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 19:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortnerapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wordlist',
            name='last_url',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]