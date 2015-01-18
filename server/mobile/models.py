from django.db import models

# Create your models here.
class Group(models.Model):
    groupID = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=30)
    groupPushTime = models.CharField(max_length=8)
    defaultValue = models.CharField(max_length=40)
    today_Value = models.CharField(max_length=40)
    owner_id = models.ForeignKey('User')
class User(models.Model):
    userID = models.CharField(max_length=10,primary_key=True)
    userName = models.CharField(max_length=8)
class Choose(models.Model):
    chooseID = models.AutoField(primary_key=True)
    chooseName = models.CharField(max_length=10)
    group = models.ForeignKey('Group')
class Day(models.Model):
    groupID = models.ForeignKey('Group')
    Mon = models.BooleanField(default=False)
    Tue = models.BooleanField(default=False)
    Wed = models.BooleanField(default=False)
    Thu = models.BooleanField(default=False)
    Fri = models.BooleanField(default=False)
    Sat = models.BooleanField(default=False)
    Sun = models.BooleanField(default=False)
class Vote(models.Model):
    userID = models.ForeignKey('User')
    chooseID = models.ForeignKey('Choose')
class Join(models.Model):
    userID = models.ForeignKey('User')
    groupID = models.ForeignKey('Group')
    isJoin = models.BooleanField(default=True)
