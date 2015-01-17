from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.db import connection
from django.utils.html import escape, strip_tags, remove_tags
from mobile.models import User

import random
STATUSCODE = {
    "ADDUSERSUCCESS":"201",
    "PARAMETERMISS":"301",
    "TOOLONGPARAMETER":"302",
    "SQLERROR":"303"
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
    if not "username" in request.POST:
        return HttpResponse(STATUSCODE["PARAMETERMISS"])
    else:
        username = escape(request.POST["username"])
        userID = getRandomString(10)
        # check if userID repet
        while User.objects.filter(userID=userID).count() > 0:
            userID = getRandomString(10)
        try:
            newUser = User(userID=userID,userName=username)
            newUser.save()
            return HttpResponse(STATUSCODE["ADDUSERSUCCESS"])
        except Exception as e:
            return HttpResponse(STATUSCODE["SQLERROR"])
            print e


