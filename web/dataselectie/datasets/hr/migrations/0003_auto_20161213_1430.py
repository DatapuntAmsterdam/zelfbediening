# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hr', '0002_cbs_sbi_hoofdcat_cbs_sbi_subcat_cbs_sbicodes'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataselectie',
            name='bag_numid',
            field=models.CharField(blank=True, db_index=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='dataselectie',
            name='bag_vbid',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
    ]
