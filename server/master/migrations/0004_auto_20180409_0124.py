# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-09 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('master', '0003_auto_20180409_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitortemplate',
            name='policy',
            field=models.ManyToManyField(to='master.MonitorNotifyPolicy', verbose_name='\u544a\u8b66\u7b56\u7565'),
        ),
    ]