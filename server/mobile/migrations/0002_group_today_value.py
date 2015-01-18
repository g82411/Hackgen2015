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
            name='today_Value',
            field=models.CharField(default=b'DEFAULT VALUE', max_length=40),
            preserve_default=True,
        ),
    ]
