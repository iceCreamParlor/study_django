# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-26 23:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0002_restaurant_location'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Restaurant',
            new_name='RestaurantLocation',
        ),
    ]
