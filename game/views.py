from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import EnterBetForm
from models import Result, Exam, GroupMember, Bet

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
            betObject = Bet(exam = examObject, target = targetObject, user = userObject, guess_mark = markInForm)
            betObject.save()
        return redirect('game.html')
    else:
        betForm = EnterBetForm()
    return render(request, 'game.html', {'betForm': betForm})

@login_required(login_url="/login/")
def joingroup_view(request):
    return render(request, 'joingroup.html')
