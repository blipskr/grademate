from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from forms import EnterBetForm, UpdateBetForm, EnterMarksForm
from models import Result, Exam, GroupMember, Bet, Group
import math
import dbqueries as query



@login_required(login_url="/login/")
def creategroup_view(request):
    return render(request, 'creategroup.html')



@login_required(login_url="/login/")
def entermarks_view(request):
    userId = request.user.id
    userGroups = query.extractGroupNames(query.retrieveUserGroupIds(userId))
    groupExams = query.retrieveGroupExams(1) # hardcoded data for now !!!CHANGE
    return render(request, 'entermarks.html', {'MarksForm' : EnterMarksForm})


@login_required(login_url="/login/")
def gamepage_view(request, gamename):
    groupid = query.extractGroupId(gamename)
    # if it is POST, either EnterBetForm or UpdateBetForm has been sent
    if request.method == 'POST':
        enterBetForm = EnterBetForm(request.POST, group=gamename)
        updateBetForm = UpdateBetForm(request.POST)
        query.processEnterBetForm(request, enterBetForm)
        query.processUpdateBetForm(request, updateBetForm)
        return redirect('/game/' + gamename)
    else:
        enterBetForm = EnterBetForm(group=gamename)
        relevantExams = []
        unprocessedExams = Exam.objects.filter(group_id=groupid).values('exam_id')
        numberofExams = 0
        for exam in unprocessedExams:
            currentexam = unprocessedExams[numberofExams]['exam_id']
            relevantExams.append(currentexam)
            numberofExams = numberofExams + 1
        yourBets = Bet.objects.filter(user=request.user.id, exam_id__in=relevantExams)
        updateBetForm = UpdateBetForm()
        betsObject = Bet.objects.filter(target=request.user.id)
        examStatsObject = query.createExamStats(betsObject)

        return render(request, 'game.html', {'yourBetsList': yourBets, 'updateBetForm': updateBetForm, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'group': gamename})

@login_required(login_url="/login/")
def joingroup_view(request):
    return render(request, 'joingroup.html')
