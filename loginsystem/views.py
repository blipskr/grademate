from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from forms import RegisterForm, LoginForm, AccountEditForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from game.models import Bet, GroupMember, Group, Exam, Result
from BetHistory import BetHistory
import re

minPasswordLength = 7
# Create your views here.


def validatePassword(password):
    if (len(password) < minPasswordLength):
        return False
    elif (re.findall('[A-Z]', password)):
        return True
    elif (re.findall('[a-z]', password)):
        return True
    elif (re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password)):
        return True
    else:
        return False


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if (not validatePassword(form.cleaned_data['password1'])):
                return registererror_view(request, form)
            else:
                form.save()
                return redirect('/login/')
        else:
            return registererror_view(request, form)
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/')
        else:
            form = LoginForm()
            return loginerror_view(request, form)
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})


def registererror_view(request, form):
    return render(request, 'registererror.html', {'form': form})


def loginerror_view(request, form):
    return render(request, 'loginerror.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url="/login/")
def profile_view(request):
    return render(request, 'profile.html',)


@login_required(login_url="/login/")
def accountsettings_view(request):
    if request.method == 'POST':
        form = AccountEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            password = form.cleaned_data['password1']
            editUser = authenticate(
                username=request.user.username, password=password)
            if editUser is not None:
                form.save()
                return redirect('/profile/')
            else:
                returnsettingsautherror_view(request, form)
        else:
            return settingsbadfielderror_view(request, form)
    else:
        form = AccountEditForm(initial={'first_name': request.user.first_name,
                                        'last_name': request.user.last_name, 'email': request.user.email})
        return render(request, 'accountsettings.html', {'form': form})


@login_required(login_url="/login/")
def settingsautherror_view(request, form):
    render(request, 'accountsettingsautherror.html', {'form': form, })


@login_required(login_url="/login/")
def settingsbadfielderror_view(request, form):
    render(request, 'accountsettingswrongfielderror.html', {'form': form})


@login_required(login_url="/login/")
def statistics_view(request):
    # get the users name
    user = request.user.username

    # GET THE GROUPS OF THE USER
    #get the users id
    userid = User.objects.filter(username=user)
    # get the users groups
    groups = GroupMember.objects.filter(user_id = userid[0].id)

    # get the group name
    idAllGroups = list()
    for group in groups:
        idAllGroups.append(group.group_id)
    groupName = list()
    for groupid in idAllGroups:
        oneGroup = Group.objects.filter(group_id = groupid)
        groupName.append(oneGroup[0].group_name)

    betObjects = Bet.objects.filter(user_id=userid[0].id)
    listOfAllBetsForAUser = list()
    for oneBetColumn in betObjects:
        try:
            resultForTarget = Result.objects.get(exam_id  = int(oneBetColumn.exam_id), user_id = int(oneBetColumn.target_id))
            resultForTarget1 = resultForTarget.mark
            exam_name_one = Exam.objects.get(exam_id = int(oneBetColumn.exam_id))
            exam_name_one = exam_name_one.exam_name
            target_user = User.objects.get(id = int(oneBetColumn.target_id))
            target_user = target_user.first_name
            if oneBetColumn.win == None:
                raise Exception()
            elif oneBetColumn.win == 1:
                oneBet = BetHistory(exam_name_one,target_user, oneBetColumn.guess_mark, resultForTarget1, 'Won')
            elif oneBetColumn.win == 0:
                oneBet = BetHistory(exam_name_one,target_user, oneBetColumn.guess_mark, resultForTarget1, 'Lose')


            listOfAllBetsForAUser.append(oneBet)
        except:
            try:
                resultForTarget = Result.objects.get(exam_id  = int(oneBetColumn.exam_id), user_id = int(oneBetColumn.target_id))
                resultForTarget1 = resultForTarget.mark
                exam_name_one = Exam.objects.get(exam_id = int(oneBetColumn.exam_id))
                exam_name_one = exam_name_one.exam_name
                target_user = User.objects.get(id = int(oneBetColumn.target_id))
                target_user = target_user.first_name
                oneBet = BetHistory(exam_name_one,target_user, oneBetColumn.guess_mark, resultForTarget1, 'Ongoing')
                listOfAllBetsForAUser.append(oneBet)
            except:
                exam_name_one = Exam.objects.get(exam_id = int(oneBetColumn.exam_id))
                exam_name_one = exam_name_one.exam_name
                target_user = User.objects.get(id = int(oneBetColumn.target_id))
                target_user = target_user.first_name
                oneBet = BetHistory(exam_name_one,target_user, oneBetColumn.guess_mark, 'Ongoing', 'Ongoing')
                listOfAllBetsForAUser.append(oneBet)



    student_lib = {
    "name": user,
    "groups" : groupName,
    "betObjects" : listOfAllBetsForAUser
    }
    return render(request, 'statistics.html', student_lib)
