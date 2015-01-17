from django.db import models

# Create your models here.
class Group(models.Model):
    gruopID = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=30)
    groupPushTime = models.CharField(max_length=8)
    defaultValue = models.DecimalField(default=0,decimal_places=10,max_digits=10)
    owner_id = models.ForeignKey('User')
class User(models.Model):
    userID = models.CharField(max_length=10,primary_key=True)
    userName = models.CharField(max_length=8)
class Choose(models.Model):
    chooseID = models.AutoField(primary_key=True)
    chooseName = models.CharField(max_length=10)
    group = models.ForeignKey('Group')


