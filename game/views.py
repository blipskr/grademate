from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm
from models import Result, Exam, GroupMember, Bet, Group
from ExamStats import ExamStats
import dbqueries as query
import math

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


@login_required(login_url="/login/")
def creategroup_view(request):
    return render(request, 'creategroup.html')

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

def extractGroupId(groupName):
    groupObject = Group.objects.filter(group_name=groupName).values('group_id')
    groupId = groupObject[0]['group_id']
    return groupId

@login_required(login_url="/login/")
def entermarks_view(request):
    userId = request.user.id
    extractGroupNames(retrieveUserGroupIds(userId))
    userExams = []
    return render(request, 'entermarks.html', )

@login_required(login_url="/login/")
def gamepage_view(request, gamename):
    groupid = extractGroupId(gamename)
    yourBets = ''
    # if it is POST, either EnterBetForm or UpdateBetForm has been sent
    if request.method == 'POST' and 'place' in request.POST:
        enterBetForm = EnterBetForm(request.POST, group=gamename)
        query.processEnterBetForm(request, enterBetForm)
        print 'test'
        return redirect('/game/' + gamename)
    elif request.method == 'POST' and 'update' in request.POST:
        updatebetform = UpdateBetForm(request.POST, bets=yourBets)
        query.processUpdateBetForm(request, updatebetform)
        return redirect('/game/' + gamename)
    else:
        enterBetForm = EnterBetForm(group=gamename)
        relevantExams = []
        unprocessedExams = Exam.objects.filter(group_id=groupid).values('exam_id')
        for exam in unprocessedExams:
            currentexam = unprocessedExams[0]['exam_id']
            relevantExams.append(currentexam)

        yourBets = Bet.objects.filter(user=request.user.id, exam_id__in=relevantExams)
        updatebetform = UpdateBetForm(bets=yourBets)
        examStatsObject = createExamStats(yourBets)
        return render(request, 'game.html', {'yourBetsList': yourBets, 'updatebetform': updatebetform, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'group': gamename})

@login_required(login_url="/login/")
def joingroup_view(request):
    return render(request, 'joingroup.html')

def getGroups(request):
    userId = request.user.id
    groups = extractGroupNames(retrieveUserGroupIds(userId))
    return groups
