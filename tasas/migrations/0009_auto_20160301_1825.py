# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-01 17:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasas', '0008_auto_20160229_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasa',
            name='tipo',
            field=models.IntegerField(choices=[(0, 'Precio por crédito'), (1, 'Pago único'), (2, 'Misceláneo')], help_text='Tipo de tasa'),
        ),
    ]
