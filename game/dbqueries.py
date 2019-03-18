from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm, EnterMarksForm
from models import Result, Exam, GroupMember, Bet, Group
from ExamStats import ExamStats
import math
import unicodedata
from django.shortcuts import render, render_to_response, redirect

# method takes as an input request
# returns a list of current users groups
def retrieveUsersGroups(request):
    usersGroups = GroupMember.objects.filter(user = request.user.id)
    return usersGroups

# method takes as an input array of Bet objects
# returns a list of ExamStats objects, each of which contains
# average bet and no of ExamStats
# on current user for each exam
def createExamStats(betsObject):
    examStatsObject = []
    tempId = 0
    # create an ExamStats object for each Bet object
    for element in betsObject:
        examStatsTemp = ExamStats(id = tempId, exam = element.exam_id, average_bet = element.guess_mark, no_of_bets = 1)
        examStatsObject.append(examStatsTemp)
        tempId += 1
    # calculate sums and numbers of elements
    for element1 in examStatsObject:
        for element2 in examStatsObject:
            if element1.id != element2.id and element1.exam == element2.exam:
                element1.average_bet += element2.average_bet
                element1.no_of_bets += 1
                #examStatsObject.remove(element2)
    # create another list, containing only unique elements
    examStatsObjects = []
    for element1 in examStatsObject:
        foundInList = False
        for element2 in examStatsObjects:
            if element1.exam == element2.exam:
                foundInList = True
        if not foundInList:
            examStatsObjects.append(element1)
    # calculate average_bet instead of sum of guesses on that exam
    for element in examStatsObjects:
        element.average_bet = math.trunc(float(element.average_bet) / element.no_of_bets)
    # return ExamStats object
    return examStatsObjects

# method takes request and betForm, processes betForm
def processEnterBetForm(request, betForm, gamename):
    examinstance = Exam.objects.get
    targetname = betForm.data['target']
    examname = betForm.data['exam']
    examid = extractExamIDgivenGroup(examname, gamename)
    targetid = getUserID(targetname)
    guessmark = betForm.data['guess_mark']
    exam = Exam.objects.get(pk=examid)
    target = User.objects.get(pk=targetid)
    newBet = Bet(exam=exam, user=request.user, target=target, guess_mark=guessmark)
    newBet.save()
    print 'ok'

# method takes request and betForm, processes UpdateBetForm
def processUpdateBetForm(request, betForm):
    print type(betForm['bet'])
    newmark = betForm.data['mark']
    betid = betForm.data['bet']
    Bet.objects.filter(pk=betid).update(guess_mark=newmark)
    return redirect('/')


# Returns list of user's group IDs which he is a member of.
def retrieveUserGroupIds(userId):
    userGroupsObject = GroupMember.objects.filter(user=userId).values('group_id')
    userGroupIdsList = []
    for element in userGroupsObject:
        groupId = element['group_id']
        userGroupIdsList.append(groupId)
    return userGroupIdsList

# Takes a list of groupIds and returns a list of corresponding groupnames
def extractGroupNames(groupIds):
    listOfGroupNames = []
    for groupId in groupIds:
        groupObject = Group.objects.filter(group_id=groupId).values('group_name')
        groupName = groupObject[0]['group_name']
        listOfGroupNames.append(groupName)
    return listOfGroupNames

# takes a name of group and returns its id
def extractGroupId(groupName):
    groupObject = Group.objects.get(group_name=groupName)
    groupId = groupObject.group_id
    return groupId

def extractExamID(examname):
    examObject = Exam.objects.get(e=examname)
    groupId = groupObject.group_id
    return groupId

def getUserID(targetname):
    userObject = User.objects.get(username=targetname)
    userID = userObject.id
    return userID

def extractExamIDgivenGroup(examname, gamename):
    groupid = extractGroupId(gamename)
    examObject = Exam.objects.get(exam_name=examname, group_id=groupid)
    examid = examObject.exam_id
    return examid

# takes an id of a group ans returns its name
def extractGroupName(groupId):
    groupObject = Group.objects.get(group_id=groupId)
    groupName = groupObject.group_name
    return groupName

# takes an id of a group and returns all the exam names associated with the group
def retrieveGroupExams(groupId):
    examObjects = Exam.objects.filter(group=groupId).values('exam_name')
    listOfExamNames = []
    for examObject in examObjects:
        examName = examObject['exam_name']
        listOfExamNames.append(examName)
    return listOfExamNames

def getGroups(request):
    userId = request.user.id
    groups = extractGroupNames(retrieveUserGroupIds(userId))
    return groups

# Takes a name of the group and returns list of tuples containing userIds and usernames respectively

def userIDsinGroup(groupName):
        groupId = Group.objects.get(group_name=groupName).group_id
        groupMemberObjects = GroupMember.objects.filter(group=groupId).values('user_id')
        userIdsList = []
        for groupObject in groupMemberObjects:
            userId = groupObject['user_id']
            uid = User.objects.get(pk=userId)
            userIdsList.append(userId)
        return userIdsList

def examIDsinGroup(groupName):
        groupId = Group.objects.get(group_name=groupName).group_id
        groupMemberObjects = Exam.objects.filter(group=groupId).values('exam_id')
        examIDsList = []
        for groupObject in groupMemberObjects:
            examID = groupObject['exam_id']
            examIDsList.append(examID)
        return examIDsList
