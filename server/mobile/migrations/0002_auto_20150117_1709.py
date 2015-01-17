# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='defaultValue',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=10),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='group',
            name='groupPushTime',
            field=models.CharField(max_length=8),
            preserve_default=True,
        ),
    ]
