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
from mobile.models import Day
from mobile.models import Join
import json
import random
STATUSCODE = {
    "ADDUSERSUCCESS":"201",
    "VOTESUCCESS":"202",
    "ADDGROUPSUCCESS":"203",
    "JOINSUCCESS":"204",
    "SEARCHSUCCESS":"206",
    "UPDATEUSERNAMESUCCESS":"205",
    "PARAMETERMISS":"301",
    "TOOLONGPARAMETER":"302",
    "SQLERROR":"303",
    "NOGROUPNAME":"304",
    "UNDEFINEUSERID":"305",
    "UNDEFINECHOOSE":"306",
    "FACKUERROR":"307",
    "UNDEFINEGROUPID":"308",
    "USERNOTINGROUP":"309",
}
def getRandomString(length):
    result = ''
    POOL = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    for i in range(length):
        result += random.choice(POOL)
    return result
# Create your views here.
def addUser(request):
    response = {}
    callback = "add_user_callback"
    if not "username" in request.GET:
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        username = escape(request.GET["username"])
        userID = getRandomString(10)
        # check if userID repet
        while User.objects.filter(userID=userID).count() > 0:
            userID = getRandomString(10)
        try:
            newUser = User(userID=userID,userName=username)
            newUser.save()
            print userID
            print username
            response["userID"] = userID
            response["userName"] = username
            response["status"] = STATUSCODE["ADDUSERSUCCESS"]
        except Exception as e:
            response["status"] = STATUSCODE["SQLERROR"]
            print e
    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
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
            if Vote.objects.filter(Q(chooseID=chooseID)&Q(userID=userID)) == 0:
                newVote = Vote(chooseID=chooseID,userID=userID)
                newVote.save()
                response["status"] = (STATUSCODE["VOTESUCCESS"])
            else:
                response["status"] = (STATUSCODE[""])
    return HttpResponse(json.dumps(response),content_type="application/json")
def viewGroup(request):
    response = {}
    callback = 'view_group_callback'
    if not "userID" in request.GET:
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        userID = request.GET["userID"]
        groupList = []
        for ids in Join.objects.filter(userID=userID).values_list('groupID','isJoin'):
            groupID = ids[0]
            isJoin = ids[1]
            groupName = Group.objects.get(groupID=groupID).groupName
            result = {"groupID":groupID,
                      "groupName":groupName,
                      "isJoin":isJoin}
            groupList.append(result)
        response["groupList"] = groupList
        response["status"] = STATUSCODE["SEARCHSUCCESS"]
    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def testFrom(request):
    response = {}
    name = request.GET["username"]
    response['aa'] = name
    data = '%s(%s);' % ('jsonCallback',json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def addGroup(request):
    response = {}
    callback = "create_group_callback"
    if not("groupname" in request.GET and "timeset" in request.GET and "defaulttoeat" in request.GET and "userID" in request.GET):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        groupName = escape(request.GET["groupname"])
        groupPushTime = escape(request.GET["timeset"])
        owner_id = User.objects.get(userID=request.GET["userID"])
        defaultValue = escape(request.GET["defaulttoeat"])
        newGroup = Group(groupName=groupName,
                         groupPushTime=groupPushTime,
                         owner_id=owner_id,
                         defaultValue=defaultValue)
        newGroup.save()
        newGroup = Group.objects.get(groupID=newGroup.groupID)
        Mon = request.GET["daysetmon"]
        Tue = request.GET["daysettue"]
        Wed = request.GET["daysetwed"]
        Thu = request.GET["daysetthu"]
        Fri = request.GET["daysetfri"]
        Sat = request.GET["daysetsat"]
        Sun = request.GET["daysetsun"]
        newDay = Day(Mon=Mon,Tue=Tue,Wed=Wed,Thu=Thu,Fri=Fri,Sat=Sat,Sun=Sun,groupID=newGroup)
        newDay.save()
        newJoin = Join(groupID=newGroup,userID=owner_id)
        newJoin.save()
        groupList = []
        for ids in Join.objects.filter(userID=owner_id).values_list('groupID','isJoin'):
            groupID = ids[0]
            isJoin = ids[1]
            groupName = Group.objects.get(groupID=groupID).groupName
            result = {"groupID":groupID,
                      "groupName":groupName,
                      "isJoin":isJoin}
            groupList.append(result)
        response["groupList"] = groupList
        response["status"] = STATUSCODE["ADDGROUPSUCCESS"]
        data = '%s(%s);' % (callback,json.dumps(response))
        return HttpResponse(data,content_type="application/javascript")
def join(request):
    callback = "join_callback"
    response = {}
    if not ("userID" in request.GET and "groupID" in request.GET):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        userID = request.GET["userID"]
        groupID = request.GET["groupID"]
        userID = User.objects.get(userID=userID)
        groupID = Group.objects.get(groupID=groupID)
        newJoin = Join(groupID=groupID,userID=userID)
        newJoin.save()
        groupList = []
        for ids in Join.objects.filter(userID=userID).values_list('groupID','isJoin'):
            groupID = ids[0]
            isJoin = ids[1]
            groupName = Group.objects.get(groupID=groupID).groupName
            result = {"groupID":groupID,
                      "groupName":groupName,
                      "isJoin":isJoin}
            groupList.append(result)
        response["groupList"] = groupList
        response["status"] = STATUSCODE["JOINSUCCESS"]
    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def parseUserID(request):
    callback = "parseUserID_callback"
    response = {}
    if not("userID" in request.GET):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    try:
        userID = request.GET["userID"]
        user = User.objects.get(userID=userID).userName
        response["userName"] = user
        response["status"] = STATUSCODE["SEARCHSUCCESS"]
    except:
        response["status"] = STATUSCODE["FACKUERROR"]

    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def updateUserName(request):
    response = {}
    callback = "update_userName_callback"
    if not("userID" in request.GET and "userName" in request.GET):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        userID = request.GET["userID"]
        userName = request.GET["userName"]
        user = User.objects.get(userID=userID)
        user.userName = escape(userName)
        user.save()
        response["status"] = STATUSCODE["UPDATEUSERNAMESUCCESS"]
        response["userName"] = escape(userName)
    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def searchGroup(request):
    response = {}
    callback = "search_group_callback"
    if not("groupID" in request.GET and "userID" in request.GET):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:

        userID = request.GET["userID"]
        groupID = request.GET["groupID"]
        searchResult = {}
        if Group.objects.filter(groupID=groupID).count() == 0:
            pass
        else:
            user = User.objects.get(userID=userID)
            group = Group.objects.get(groupID=groupID)
            day = Day.objects.get(groupID=group)
            print group.owner_id.userID
            owner = User.objects.get(userID=group.owner_id.userID).userName
            searchResult["mon"] = day.Mon
            searchResult["tue"] = day.Tue
            searchResult["wed"] = day.Wed
            searchResult["thu"] = day.Thu
            searchResult["fri"] = day.Fri
            searchResult["sat"] = day.Sat
            searchResult["sun"] = day.Sun
            searchResult["groupID"] = group.groupID
            searchResult["groupName"] = group.groupName
            searchResult["groupPushTime"] = group.groupPushTime
            searchResult["defaultValue"] = group.defaultValue
            searchResult["owner"] = owner
            if Join.objects.filter(Q(userID=user) & Q(groupID=group)).count() == 0:
                searchResult["isJoin"] = False
            else:
                searchResult["isJoin"] = True
            response.update(searchResult)
            response["status"] = STATUSCODE["SEARCHSUCCESS"]

    response["status"] = STATUSCODE["FACKUERROR"]
    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def viewChoose(request):
    response = {}
    callback = "view_choose_callback"
    if not('userID' in request.GET and 'groupID' in request.GET):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        groupID = request.GET["groupID"]
        userID = request.GET["userID"]
        if not (groupID and userID):
            response["status"] = STATUSCODE["PARAMETERMISS"]
        elif Group.objects.filter(groupID=groupID).count() == 0:
            response["status"] = STATUSCODE["UNDEFINEGROUPID"]
        elif User.objects.filter(userID=userID).count() == 0:
            response["status"] = STATUSCODE["UNDEFINEUSERID"]
        elif Join.objects.filter(Q(userID=User.objects.get(userID=userID)) & Q(groupID=Group.objects.get(groupID=groupID))).count == 0:
            response["status"] = STATUSCODE["USERNOTINGROUP"]
        else:
            searchResult = []
            chooseList = Choose.objects.filter(group_id=Group.objects.get(groupID=groupID))
            if chooseList.count() == 0:
                pass
            else:
                for choose in chooseList.values_List('chooseID' , 'chooseName'):
                    chooseID = choose[0]
                    chooseName = choose[1]
                    if Vote.objects.filter(Q(userID_id=userID) & Q(chooseID_id=chooseID)):
                        result = {"id":chooseID , "name":chooseName,"isVote":True}
                    else:
                        result = {"id":chooseID , "name":chooseName,"isVote":False}
                    voteNumber = Vote.objects.filter(chooseID_id=chooseID).count()
                    result["voteNumber"] = voteNumber
                    searchResult.append(result)
                response["chooseList"] = searchResult
                response["status"] = STATUSCODE["SEARCHSUCCESS"]
    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")
def addChoose(request):
    response = {}
    callback = "view_choose_callback"
    if not('userID' in request.GET and 'groupID' in request.GET and 'chooseName' in request.GET):
        response["status"] = STATUSCODE["PARAMETERMISS"]
    else:
        groupID = request.GET["groupID"]
        userID = request.GET["userID"]
        chooseName = request.GET["chooseName"]
        if not (groupID and userID and chooseName):
            response["status"] = STATUSCODE["PARAMETERMISS"]
        elif Group.objects.filter(groupID=groupID).count() == 0:
            response["status"] = STATUSCODE["UNDEFINEGROUPID"]
        elif User.objects.filter(userID=userID).count() == 0:
            response["status"] = STATUSCODE["UNDEFINEUSERID"]
        elif Join.objects.filter(Q(userID=User.objects.get(userID=userID)) & Q(groupID=Group.objects.get(groupID=groupID))).count == 0:
            response["status"] = STATUSCODE["USERNOTINGROUP"]
        else:
            groupID = Group.objects.get(groupID=groupID)
            newChoose = Choose(chooseName=chooseName,group=groupID)
            newChoose.save()
            userID = User.objects.get(userID=userID)
            newVote = Vote(userID=userID,chooseID_id=newChoose.chooseID)
            newVote.save()
            searchResult = []
            chooseList = Choose.objects.filter(groupID=groupID)
            if chooseList.count() == 0:
                pass
            else:
                for choose in chooseList.values_List('chooseID' , 'chooseName'):
                    chooseID = choose[0]
                    chooseName = choose[1]
                    if Vote.objects.filter(Q(userID=userID) & Q(chooseID_id=chooseID)):
                        result = {"id":chooseID , "name":chooseName,"isVote":True}
                    else:
                        result = {"id":chooseID , "name":chooseName,"isVote":False}
                    voteNumber = Vote.objects.filter(chooseID_id=chooseID).count()
                    result["voteNumber"] = voteNumber
                    searchResult.append(result)
                response["chooseList"] = searchResult
                response["status"] = STATUSCODE["SEARCHSUCCESS"]
    data = '%s(%s);' % (callback,json.dumps(response))
    return HttpResponse(data,content_type="application/javascript")








