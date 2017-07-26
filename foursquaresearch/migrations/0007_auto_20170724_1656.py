# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 13:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foursquaresearch', '0006_usersearch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersearch',
            name='id',
        ),
        migrations.AddField(
            model_name='usersearch',
            name='auto_increment_id',
            field=models.AutoField(default='000', primary_key=True, serialize=False),
        ),
        migrations.RemoveField(
            model_name='usersearch',
            name='user',
        ),
        migrations.AddField(
            model_name='usersearch',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]