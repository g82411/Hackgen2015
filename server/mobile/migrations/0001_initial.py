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
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('groupID', models.AutoField(serialize=False, primary_key=True)),
                ('groupName', models.CharField(max_length=30)),
                ('groupPushTime', models.CharField(max_length=8)),
                ('defaultValue', models.CharField(max_length=40)),
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
        migrations.AddField(
            model_name='join',
            name='userID',
            field=models.ForeignKey(to='mobile.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='owner_id',
            field=models.ForeignKey(to='mobile.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='day',
            name='groupID',
            field=models.ForeignKey(to='mobile.Group'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='choose',
            name='group',
            field=models.ForeignKey(to='mobile.Group'),
            preserve_default=True,
        ),
    ]
