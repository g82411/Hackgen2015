from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connection
from django.utils.html import escape, strip_tags, remove_tags
from mobile.models import User
from mobile.models import Group
import json
import random
STATUSCODE = {
    "ADDUSERSUCCESS":"201",
    "PARAMETERMISS":"301",
    "TOOLONGPARAMETER":"302",
    "SQLERROR":"303",
    "NOGROUPNAME":"304",
    "UNDEFINEUSERID":"305"
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
    if User.objects.filer(userID=userID).count() == 0:
        response["status"] = (STATUSCODE["UNDEFINEUSERID"])
    else:
        userName = User.objects.get(userID=userID)
        response["username"] = userName
    return HttpResponse(json.dumps(response),content_type="application/json")









