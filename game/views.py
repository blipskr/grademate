from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Result, Exam, GroupMember

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
    return render(request, 'game.html')

@login_required(login_url="/login/")
def joingroup_view(request):
    return render(request, 'joingroup.html')
