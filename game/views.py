from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm, EnterMarksForm, ViewMarksForm, CreateGroupForm, AddExamForm, JoinGroupForm
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


@login_required(login_url="/login/")
def creategroup_view(request):
    return render(request, 'creategroup.html')


@login_required(login_url="/login/")
def entermarks_view(request, gamename):
    userId = request.user.id
    groupId = Group.objects.get(group_name=gamename)
    groupExams = query.retrieveGroupExams(groupId)
    # if it is POST, EnterMarksForm has been sent
    if request.method == 'POST':
        enterMarksForm = EnterMarksForm(request.POST, group=gamename)
        if enterMarksForm.is_valid():
            resultsObject = enterMarksForm.save(commit=False)
            resultsObject.user = request.user
            resultsObject.save()
            # redirect to clear the form after saving
            return redirect('/game/' + gamename + '/entermarks/')
        else:
            # render to display the error
            return render(request, 'entermarks.html', {'EnterMarksForm': enterMarksForm, 'group': gamename})
    else:
        enterMarksForm = EnterMarksForm(group=gamename)
        viewMarksForm = ViewMarksForm(group=gamename)
        return render(request, 'entermarks.html', {'EnterMarksForm': enterMarksForm, 'ViewMarksForm': viewMarksForm, 'group': gamename})


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
        return render(request, 'game.html', {'yourBetsList': yourBets, 'updatebetform': updatebetform, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'group': gamename})



@login_required(login_url="/login/")

def getGroups(request):
    userId = request.user.id
    groups = extractGroupNames(retrieveUserGroupIds(userId))
    return groups

# method to check if given user is admin of given group
def userIsAdminOfGroup(userId, groupId):
    groupObject = Group.objects.get(group_id = groupId)
    groupAdmin = GroupMember.objects.order_by(id).first()
    adminId = groupAdmin.id
    if userId == adminId:
        return true
    else:
        return false

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
    # if it is POST, EnterMarksForm has been sent
    if request.method == 'POST':
        addExamForm = AddExamForm(request.POST)
        if addExamForm.is_valid():
            exam_name = addExamForm.data['exam_name']
            query.createNewExam(exam_name, gamename)
            # redirect to clear the form after saving
            return redirect('/game/' + gamename + '/managegroup/')
        else:
            # render to display the error
            return render(request, 'managegroup.html', {'addexam': addExamForm, 'groupName': gamename})
    else:
        addExamForm = AddExamForm()
        return render(request, 'managegroup.html', {'addexam': addExamForm, 'groupName': gamename})

@login_required(login_url="/login/")
def joingroup_view(request):
    if request.method == 'POST':
        return query.processJoinGroupForm(request)
    else:
        form = JoinGroupForm(request.POST)
        return render(request, 'joingroup.html', { 'form': form })
