# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mobile', '0002_auto_20150117_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('Mon', models.BooleanField(default=False)),
                ('Tue', models.BooleanField(default=False)),
                ('Wed', models.BooleanField(default=False)),
                ('Thu', models.BooleanField(default=False)),
                ('Fri', models.BooleanField(default=False)),
                ('Sat', models.BooleanField(default=False)),
                ('Sun', models.BooleanField(default=False)),
                ('groupID', models.ForeignKey(to='mobile.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Join',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('isJoin', models.BooleanField(default=True)),
                ('groupID', models.ForeignKey(to='mobile.Group')),
                ('userID', models.ForeignKey(to='mobile.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chooseID', models.ForeignKey(to='mobile.Choose')),
                ('userID', models.ForeignKey(to='mobile.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
