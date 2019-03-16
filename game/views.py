from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm
from models import Result, Exam, GroupMember, Bet
from ExamStats import ExamStats
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

# method takes request and betForm, processes betForm
def processEnterBetForm(request, betForm):
    targetInForm = betForm.cleaned_data['user']
    examInForm = betForm.cleaned_data['exam']
    markInForm = betForm.cleaned_data['mark']
    examObject = Exam.objects.get(exam_id=examInForm)
    targetObject = User.objects.get(id=targetInForm)
    userObject = User.objects.get(id=request.user.id)
    if targetObject.id != request.user.id:
        betObject = Bet(exam = examObject, target = targetObject, user = userObject, guess_mark = markInForm)
        betObject.save()

# method takes request and betForm, processes UpdateBetForm
def processUpdateBetForm(request, betForm):
    markInForm = betForm.cleaned_data['mark']
    yourBets = Bet.objects.filter(user=request.user.id)

# Create your views here.
@login_required(login_url="/login/")
def creategroup_view(request):
    userName = request.user.username
    userId = User.objects.filter(username=userName).values('id')
    userGroups = GroupMember.objects.filter(user=userId).values('group_id').distinct()
    userExams = []
    for aGroup in userGroups:
        groupExams = Exam.objects.filter(group=aGroup).values('group_id').distinct()
        userExams.extend(groupExams)

    return render(request, 'creategroup.html')

@login_required(login_url="/login/")
def entermarks_view(request):
    return render(request, 'entermarks.html')

@login_required(login_url="/login/")
def gamepage_view(request):
    # if it is POST, either EnterBetForm or UpdateBetForm has been sent
    if request.method == 'POST':
        enterBetForm = EnterBetForm(request.POST)
        updateBetForm = UpdateBetForm(request.POST)
        if enterBetForm.is_valid():
            processEnterBetForm(request, enterBetForm)
        elif updateBetForm.is_valid():
            processUpdateBetForm(request, updateBetForm)
        return redirect('game.html')
    else:
        enterBetForm = EnterBetForm()
    yourBets = Bet.objects.filter(user=request.user.id)
    updateBetForm = UpdateBetForm()
    betsObject = Bet.objects.filter(target=request.user.id)
    examStatsObject = createExamStats(betsObject)
    usersGroups = retrieveUsersGroups(request)
    return render(request, 'game.html', {'yourBetsList': yourBets, 'updateBetForm': updateBetForm, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'yourGroups': usersGroups})

@login_required(login_url="/login/")
def joingroup_view(request):
    return render(request, 'joingroup.html')
