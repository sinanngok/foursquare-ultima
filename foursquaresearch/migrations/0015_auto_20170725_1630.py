# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 13:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foursquaresearch', '0014_auto_20170725_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fav',
            old_name='name',
            new_name='place_name',
        ),
    ]