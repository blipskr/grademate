from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm, EnterMarksForm, JoinGroupForm
from models import Result, Exam, GroupMember, Bet, Group
from ExamStats import ExamStats
import math
import unicodedata
from django.shortcuts import render, render_to_response, redirect

# method takes as an input request
# returns a list of current users groups


def retrieveUsersGroups(request):
    usersGroups = GroupMember.objects.filter(user=request.user.id)
    return usersGroups

# method takes as an input array of Bet objects
# returns a list of ExamStats objects, each of which contains
# average bet and no of ExamStats
# on current user for each exam

def examIDtoName(examid):
    examObject = Exam.objects.get(pk=examid)
    examName = examObject.exam_name
    return examName

def createExamStats(betsObject):
    examStatsObject = []
    tempId = 0
    # create an ExamStats object for each Bet object
    for element in betsObject:
        examStatsTemp = ExamStats(
            id=tempId, exam=element.exam_id, average_bet=element.guess_mark, no_of_bets=1)
        examStatsObject.append(examStatsTemp)
        tempId += 1
    # calculate sums and numbers of elements
    for element1 in examStatsObject:
        for element2 in examStatsObject:
            if element1.id != element2.id and element1.exam == element2.exam:
                element1.average_bet += element2.average_bet
                element1.no_of_bets += 1
                # examStatsObject.remove(element2)
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
        element.average_bet = math.trunc(
            float(element.average_bet) / element.no_of_bets)
    # return ExamStats object
    return examStatsObjects

# method takes request and betForm, processes betForm

def processJoinGroupForm(request):
    form = JoinGroupForm(request.POST)
    group_name = form.data['group_name']
    group_id = form.data['group_id']
    try:
        group = Group.objects.get(pk=group_id)
        if (GroupMember.objects.filter(user=request.user, group=group).count() == 0):
            if (int(extractGroupId(group_name)) == int(group_id)):
                    newGroupMember = GroupMember(group=group, user=request.user, credits=100)
                    newGroupMember.save()
                    return redirect('/game/' + group_name)
            else:
                    return render(request, 'groupnotfounderror.html', {'form': form})
        else:
            return render(request, 'alreadyingrouperror.html', {'form': form} )
    except:
        return render(request, 'groupnotfounderror.html', {'form': form})

def processEnterMarksForm(request, enterMarksForm, gamename):
    print 'sth'
    examId = enterMarksForm.data['exam']
    exam = Exam.objects.get(pk=examId)
    enteredMark = enterMarksForm.data['mark']
    if not (int(enteredMark) >= 0 and int(enteredMark) <= 100):
        print 'notsaved'
        return render(request, 'invalidmark.html', {'EnterMarksForm' : EnterMarksForm(group=gamename), 'group' : gamename})
    else:
        print 'saved'
        newResult = Result(exam=exam, user=request.user, mark=enteredMark)
        newResult.save()
        return redirect('/game/' + gamename + '/entermarks/')




def processEnterBetForm(request, betForm, gamename):
    examinstance = Exam.objects.get
    targetname = betForm.data['target']
    examname = betForm.data['exam']
    examid = extractExamIDgivenGroup(examname, gamename)
    targetid = getUserID(targetname)
    guessmark = betForm.data['guess_mark']
    exam = Exam.objects.get(pk=examid)
    target = User.objects.get(pk=targetid)
    newBet = Bet(exam=exam, user=request.user,
                 target=target, guess_mark=guessmark)
    newBet.save()

# method takes request and betForm, processes UpdateBetForm


def processUpdateBetForm(request, betForm):
    newmark = betForm.data['mark']
    targetname = betForm.data['bet']
    targetid = getUserID(targetname)
    target = User.objects.get(pk=targetid)
    user = request.user
    Bet.objects.filter(user=user, target=target).update(guess_mark=newmark)
    return redirect('/')

# Returns list of user's group IDs which he is a member of.


def retrieveUserGroupIds(userId):
    userGroupsObject = GroupMember.objects.filter(
        user=userId).values('group_id')
    userGroupIdsList = []
    for element in userGroupsObject:
        groupId = element['group_id']
        userGroupIdsList.append(groupId)
    return userGroupIdsList

# Takes a list of groupIds and returns a list of corresponding groupnames


def extractGroupNames(groupIds):
    listOfGroupNames = []
    for groupId in groupIds:
        groupObject = Group.objects.filter(
            group_id=groupId).values('group_name')
        groupName = groupObject[0]['group_name']
        listOfGroupNames.append(groupName)
    return listOfGroupNames

# takes a name of group and returns its id

def extractGroupId(groupName):
    try:
        groupObject = Group.objects.get(group_name=groupName)
        groupId = groupObject.group_id
        return groupId
    except Group.DoesNotExist:
        return None


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
    groupMemberObjects = GroupMember.objects.filter(
        group=groupId).values('user_id')
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

# Creates a new group with given name
def createNewGroup(groupName):
    groupObject = Group(group_name = groupName)
    groupObject.save()

# creates new exam with given name for given group
def createNewExam(examName, groupName):
    try:
        examObject = Exam.objects.get(exam_name = examName)
    # if exam does not exist, create it
    except Exam.DoesNotExist:
        groupObject = Group.objects.get(group_name = groupName)
        examObject = Exam(group = groupObject, exam_name = examName)
        examObject.save()

# adds given user to the given group by name
def addUserToGroup(user_name, groupName):
    print "addUserToGroup1"
    try:
        print "try"
        userObject = User.objects.get(username = user_name)
        groupMemberObject = GroupMember.objects.get(user = userObject)
        print "try succeeded"
    # if GroupMember does not exist, create it
    except GroupMember.DoesNotExist:
        print "except processing"
        groupObject = Group.objects.get(group_name = groupName)
        userObject = User.objects.get(username = user_name)
        groupMemberObject = GroupMember(group = groupObject, user = userObject, credits = 100)
        groupMemberObject.save()
        print "except succeeded"

# method to delete user from the group
def removeUserFromGroup(userName, groupName):
    # determine groupObject, userObject, betObjects, resultObjects, groupMemberObject
    userObject = User.objects.get(username = userName)
    groupObject = Group.objects.get(group_name = groupName)
    groupMemberObject = GroupMember.objects.get(group = groupObject, user = userObject)
    betObjects1 = Bet.objects.filter(target = userObject)
    betObjects2 = Bet.objects.filter(user = userObject)
    # delete it
    groupMemberObject.delete()
    betObjects1.delete()
    betObjects2.delete()

# method to delete exam from the group
def removeExamFromGroup(examName, groupName):
    # determine groupObject, examObject, betObjects and resultObjects
    groupObject = Group.objects.get(group_name = groupName)
    examObject = Exam.objects.get(exam_name = examName, group = groupObject)
    betObjects = Bet.objects.filter(exam = examObject)
    resultObjects = Result.objects.filter(exam = examObject)
    # delete it
    betObjects.delete()
    examObject.delete()
    resultObjects.delete()

# method to check if given user is creator (admin) of the group
# returns true if he is
def userIsAdminOfGroup(userObject, groupName):
    #userObject = User.objects.get(username = userName)
    groupObject = Group.objects.get(group_name = groupName)
    groupMemberObjects = GroupMember.objects.filter(group = groupObject)
    groupAdminObject = groupMemberObjects[0]
    groupMemberObject = GroupMember.objects.get(group = groupObject, user = userObject)
    if groupAdminObject is groupMemberObject:
        return True
    else:
        return False

# method to check if given user is a member of given group
def userIsMemberOfGroup(userName, groupName):
    userObject = User.objects.get(username = userName)
    groupObject = Group.objects.get(group_name = groupName)
    try:
        groupMemberObject = GroupMember.objects.get(group = groupObject, user = userObject)
        return True
    except GroupMember.DoesNotExist:
        return False
