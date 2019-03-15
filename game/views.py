from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import EnterBetForm
from models import Result, Exam, GroupMember, Bet, ExamStats
import math

# method takes as an input array of Bet objects
# returns a list of ExamStats objects, each of which contains
# average bet and no of ExamStats
# on current user for each exam
def createExamStats(betsObject):
    examStatsObject = []
    tempId = 0
    # create an ExamStats object for each Bet object
    for element in betsObject:
        examStatsTemp = ExamStats(id = tempId, exam = element.exam, average_bet = element.guess_mark, no_of_bets = 1)
        examStatsObject.append(examStatsTemp)
        tempId += 1
    # make each exam in examStatsObject unique
    # that is, delete repeating elements
    for element1 in examStatsObject:
        for element2 in examStatsObject:
            if element1.id != element2.id and element1.exam == element2.exam:
                element1.average_bet += element2.average_bet
                element1.no_of_bets += 1
                examStatsObject.remove(element2)

    # calculate average_bet instead of sum of guesses on that exam
    for element in examStatsObject:
        element.average_bet = math.trunc(float(element.average_bet) / element.no_of_bets)
    # return ExamStats object
    return examStatsObject

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
    if request.method == 'POST':
        betForm = EnterBetForm(request.POST)
        if betForm.is_valid():
            targetInForm = betForm.cleaned_data['user']
            examInForm = betForm.cleaned_data['exam']
            markInForm = betForm.cleaned_data['mark']
            examObject = Exam.objects.get(exam_id=examInForm)
            targetObject = User.objects.get(id=targetInForm)
            userObject = User.objects.get(id=request.user.id)
            if targetInForm != request.user.id:
                betObject = Bet(exam = examObject, target = targetObject, user = userObject, guess_mark = markInForm)
                betObject.save()
        return redirect('game.html')
    else:
        betForm = EnterBetForm()
    betsObject = Bet.objects.filter(target=request.user.id)
    examStatsObject = createExamStats(betsObject)
    return render(request, 'game.html', {'betForm': betForm, 'betsListOnYou': examStatsObject})

@login_required(login_url="/login/")
def joingroup_view(request):
    return render(request, 'joingroup.html')
