# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choose',
            fields=[
                ('chooseID', models.AutoField(serialize=False, primary_key=True)),
                ('chooseName', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('gruopID', models.AutoField(serialize=False, primary_key=True)),
                ('groupName', models.CharField(max_length=30)),
                ('groupPushTime', models.TimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userID', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('userName', models.CharField(max_length=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='group',
            name='owner_id',
            field=models.ForeignKey(to='mobile.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choose',
            name='group',
            field=models.ForeignKey(to='mobile.Group'),
            preserve_default=True,
        ),
    ]
