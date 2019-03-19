from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm, EnterMarksForm, CreateGroupForm, AddExamForm, JoinGroupForm, AddUserToGroupForm
from django.contrib.auth import login
from models import Result, Exam, GroupMember, Bet, Group
from ExamStats import ExamStats
import dbqueries as query
import math
from django.core.exceptions import ValidationError

# method takes as an input array of Bet objects
# returns a list of ExamStats objects, each of which contains
# average bet and no of ExamStats
# on current user for each exam


def createExamStats(betsObject):
    examStatsObject = []
    tempId = 0
    # create an ExamStats object for each Bet object
    for element in betsObject:
        exam_name = query.examIDtoName(element.exam_id)
        examStatsTemp = ExamStats(
            id=tempId, exam_id=element.exam_id, average_bet=element.guess_mark, no_of_bets=1, exam_name = exam_name)
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

@login_required(login_url="/login/")
def entermarks_view(request, gamename):
    userId = request.user.id
    groupId = Group.objects.get(group_name=gamename)
    groupExamIds = query.examIDsinGroup(gamename)
    userResults = Result.objects.filter(
        user=request.user.id, exam_id__in=groupExamIds)
    # if it is POST, EnterMarksForm has been sent
    if request.method == 'POST':
        enterMarksForm = EnterMarksForm(request.POST, group=groupId)
        return query.processEnterMarksForm(request, enterMarksForm, gamename)
    else:
        enterMarksForm = EnterMarksForm(group=groupId)
        return render(request, 'entermarks.html', {'EnterMarksForm': enterMarksForm, 'group': gamename, 'userResultsList' : userResults})


@login_required(login_url="/login/")
def gamepage_view(request, gamename):
    groupid = query.extractGroupId(gamename)
    yourBets = ''
    # if it is POST, either EnterBetForm or UpdateBetForm has been sent
    if request.method == 'POST' and 'place' in request.POST:
        enterBetForm = EnterBetForm(
            request.POST, group=gamename, user=request.user)
        query.processEnterBetForm(request, enterBetForm, gamename)
        return redirect('/game/' + gamename)
    elif request.method == 'POST' and 'update' in request.POST:
        updatebetform = UpdateBetForm(request.POST, bets=yourBets)
        query.processUpdateBetForm(request, updatebetform)
        return redirect('/game/' + gamename)
    else:
        enterBetForm = EnterBetForm(group=gamename, user=request.user)
        relevantExams = []
        unprocessedExams = Exam.objects.filter(
            group_id=groupid).values('exam_id')
        examCount = 0
        for exam in unprocessedExams:
            currentexam = unprocessedExams[examCount]['exam_id']
            relevantExams.append(currentexam)
            examCount = examCount + 1
        yourBets = Bet.objects.filter(
            user=request.user.id, exam_id__in=relevantExams)
        updatebetform = UpdateBetForm(bets=yourBets)
        examStatsObject = createExamStats(yourBets)
        if query.userIsAdminOfGroup(request.user, groupid):
            return render(request, 'gamewithadmin.html', {'yourBetsList': yourBets, 'updatebetform': updatebetform, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'group': gamename})
        else:
            return render(request, 'game.html', {'yourBetsList': yourBets, 'updatebetform': updatebetform, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'group': gamename})


@login_required(login_url="/login/")

def getGroups(request):
    userId = request.user.id
    groups = extractGroupNames(retrieveUserGroupIds(userId))
    return groups


@login_required(login_url="/login/")
def creategroup_view(request):
    # if sent a form of creating a group, process it
    if request.method == 'POST':
        createGroupForm = CreateGroupForm(request.POST)
        # create a new group with given name
        if createGroupForm.is_valid():
            groupName = createGroupForm.data['group_name']
            if query.extractGroupId(groupName) == None:
                query.createNewGroup(groupName)
                username = User.objects.get(id = request.user.id)
                query.addUserToGroup(username, groupName)
                # redirect to managegroup.html
                return redirect('/game/' + groupName + '/managegroup/')
                #return managegroup_view(request, groupName)
            else:
                createGroupForm = CreateGroupForm()
    #  if we just open the page, give this page
    else:
        createGroupForm = CreateGroupForm()
    return render(request, 'creategroup.html', {'form': createGroupForm})

@login_required(login_url="/login/")
def managegroup_view(request, gamename):
    groupid = query.extractGroupId(gamename)
    # if user is not admin, redirect to gamepage
    currentUser = User.objects.get(id = request.user.id)
    if request.method == 'POST' and 'addexam' in request.POST:
        addExamForm = AddExamForm(request.POST)
        if addExamForm.is_valid():
            exam_name = addExamForm.data['exam_name']
            query.createNewExam(exam_name, gamename)
            # redirect to clear the form after saving
            return redirect('/game/' + gamename + '/managegroup/')
        else:
            # render to display the error
            return render(request, 'managegroup.html', {'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm})
    elif request.method == 'POST' and 'adduser' in request.POST:
        addUserForm = AddUserToGroupForm(request.POST)
        if addUserForm.is_valid():
            user_name = addUserForm.data['user_name']
            query.addUserToGroup(user_name, gamename)
            return redirect('/game/' + gamename + '/managegroup/')
        else:
            return render(request, 'managegroup.html', {'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm})
    else:
        addExamForm = AddExamForm()
        addUserForm = AddUserToGroupForm()
        return render(request, 'managegroup.html', {'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm})

@login_required(login_url="/login/")
def joingroup_view(request):
    if request.method == 'POST':
        return query.processJoinGroupForm(request)
    else:
        form = JoinGroupForm(request.POST)
        return render(request, 'joingroup.html', { 'form': form })
