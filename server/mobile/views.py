# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connection
from django.utils.html import escape, strip_tags, remove_tags
from mobile.models import User
from mobile.models import Group
from mobile.models import Choose
from mobile.models import Vote
from mobile.models import Join
import json
import random
STATUSCODE = {
    "ADDUSERSUCCESS":"201",
    "VOTESUCCESS":"202",
    "PARAMETERMISS":"301",
    "TOOLONGPARAMETER":"302",
    "SQLERROR":"303",
    "NOGROUPNAME":"304",
    "UNDEFINEUSERID":"305",
    "UNDEFINECHOOSE":"306"
}
def getRandomString(length):
    result = ''
    POOL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    for i in range(length):
        result += random.choice(POOL)
    return result
# Create your views here.
@csrf_exempt
def addUser(request):
    response = {}
    if not "username" in request.POST:
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        username = escape(request.POST["username"])
        userID = getRandomString(10)
        # check if userID repet
        while User.objects.filter(userID=userID).count() > 0:
            userID = getRandomString(10)
        try:
            newUser = User(userID=userID,userName=username)
            newUser.save()
            response["status"] = STATUSCODE["ADDUSERSUCCESS"]
        except Exception as e:
            response["status"] = STATUSCODE["SQLERROR"]
            print e
        return HttpResponse(json.dumps(response),content_type="application/json")
def viewUserName(request):
    response = {}
    if not "userID" in request.GET:
        response["status"] = STATUSCODE["PARAMETERMISS"]
    userID = request.GET["userID"]
    # check if userid is not in db
    if User.objects.filter(userID=userID).count() == 0:
        response["status"] = (STATUSCODE["UNDEFINEUSERID"])
    else:
        userName = User.objects.get(userID=userID).userName
        response["username"] = userName
    return HttpResponse(json.dumps(response),content_type="application/json")
def vote(request):
    response = {}
    if not ("userID" in request.POST and "chooseID" in request.POST):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        userID = request.POST["userID"]
        chooseID = request.POST["chooseID"]
        if User.objects.filter(userID=userID).count() == 0:
            response["status"] = (STATUSCODE["UNDEFINEUSERID"])
        elif Choose.objects.filter(userID=userID).count() == 0:
            response["status"] = (STATUSCODE["UNDEFINECHOOSE"])
        else:
            chooseID = Choose.objects.get(chooseID=chooseID)
            userID = User.objects.get(userID=userID)
            newVote = vote(chooseID=chooseID,userID=userID)
            newVote.save()
            response["status"] = (STATUSCODE["VOTESUCCESS"])
    return HttpResponse(json.dumps(response),content_type="application/json")

def viewGroup(request):
    response = {}
    if not "userID" in request.GET:
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        userID = request.GET["userID"]
        for groupid in Join.objects.filter(userID=userID).values_list('groupID'):
            pass
def testFrom(request):
    response = {}
    userName = User.objects.get(userID="5wdmkf0xKM").userName
    response['aa'] = userName
    if 'callback' in request.REQUEST:
        data = '%s(%s);' % ('jsonCallback',json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def addGroup(request):
    for key in request.POST:
        print request.POST[key]














