# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 14:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foursquaresearch', '0007_auto_20170724_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersearch',
            name='user',
        ),
        migrations.AddField(
            model_name='usersearch',
            name='user_id',
            field=models.IntegerField(default='000'),
        ),
    ]