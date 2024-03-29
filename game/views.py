from django.shortcuts import render, render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm, EnterMarksForm, CreateGroupForm, AddExamForm, JoinGroupForm, AddUserToGroupForm, DeleteExamForm, DeleteUserForm
from django.contrib.auth import login
from models import Result, Exam, GroupMember, Bet, Group
from ExamStats import ExamStats
import dbqueries as query
import math
from LeaderBoardClass import LeaderBoardClass
from django.core.exceptions import ValidationError


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
        error = query.processEnterMarksForm(request, enterMarksForm, gamename)
        enterMarksForm = EnterMarksForm(group=groupId)
    else:
        enterMarksForm = EnterMarksForm(group=groupId)
        error = False

    return render(request, 'entermarks.html', {'error' : error, 'EnterMarksForm': enterMarksForm, 'group': gamename, 'userResultsList': userResults})


@login_required(login_url="/login/")
def gamepage_view(request, gamename):
    groupid = query.extractGroupId(gamename)
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
        user=request.user.id, exam_id__in=relevantExams).order_by('exam')
    updatebetform = UpdateBetForm(bets=yourBets)
    betsOnYou = Bet.objects.filter(
        target=request.user.id, exam_id__in=relevantExams).order_by('exam')
    examStatsObject = query.createExamStats(betsOnYou)

    # leaderboard code groupid, name, credits query.getUserID(request.user)
    allUsersInGroup = GroupMember.objects.filter(group_id = groupid).order_by('-credits')
    infoLeaderBoard = list()
    counter = 1
    for member in allUsersInGroup:
        noOfWins = Bet.objects.filter(user_id = member.user_id, win = 1)
        oneLeaderBoard = LeaderBoardClass(counter, query.getUserName(member.user_id), member.credits, len(noOfWins))
        counter = counter + 1
        infoLeaderBoard.append(oneLeaderBoard)


    # if it is POST, either EnterBetForm or UpdateBetForm has been sent
    if request.method == 'POST' and 'place' in request.POST:
        enterBetForm = EnterBetForm(
            request.POST, group=gamename, user=request.user)
        error = query.processEnterBetForm(request, enterBetForm, gamename)
        enterBetForm = EnterBetForm(group=gamename, user=request.user)
        yourBets = Bet.objects.filter(
            user=request.user.id, exam_id__in=relevantExams, win = None).order_by('exam')
        updatebetform = UpdateBetForm(bets=yourBets)
    elif request.method == 'POST' and 'update' in request.POST:
        updatebetform = UpdateBetForm(request.POST, bets=yourBets)
        error = query.processUpdateBetForm(request, updatebetform)
        enterBetForm = EnterBetForm(group=gamename, user=request.user)
        yourBets = Bet.objects.filter(
            user=request.user.id, exam_id__in=relevantExams, win = None).order_by('exam')
        updatebetform = UpdateBetForm(bets=yourBets)
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
            user=request.user.id, exam_id__in=relevantExams, win = None).order_by('exam')
        updatebetform = UpdateBetForm(bets=yourBets)
        betsOnYou = Bet.objects.filter(
            target=request.user.id, exam_id__in=relevantExams).order_by('exam')
        examStatsObject = query.createExamStats(betsOnYou)
        error = False
    credits = GroupMember.objects.get(group_id = groupid, user_id= query.getUserID(request.user))
    return render(request, 'game.html', {'error': error, 'admin': query.userIsAdminOfGroup(request.user, groupid), 'yourBetsList': yourBets, 'updatebetform': updatebetform, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'group': gamename, 'credits': credits.credits, 'leaderBoard': infoLeaderBoard})


@login_required(login_url="/login/")
def getGroups(request):
    userId = request.user.id
    groups = extractGroupNames(retrieveUserGroupIds(userId))
    return groups


@login_required(login_url="/login/")
def creategroup_view(request):
    # if sent a form of creating a group, process it
    error = False
    if request.method == 'POST':
        createGroupForm = CreateGroupForm(request.POST)
        # create a new group with given name
        if createGroupForm.is_valid():
            groupName = createGroupForm.data['group_name']
            if query.extractGroupId(groupName) == None:
                query.createNewGroup(request.user.username, groupName)
                username = User.objects.get(id=request.user.id)
                query.addUserToGroup(username, groupName)
                # redirect to managegroup.html
                return redirect('/game/' + groupName + '/managegame/')
                # return managegroup_view(request, groupName)
            else:
                createGroupForm = CreateGroupForm()
                error = 'Group with this name already exists.'
    #  if we just open the page, give this page
    else:
        createGroupForm = CreateGroupForm()
    return render(request, 'creategroup.html', {'error' : error, 'form': createGroupForm})


@login_required(login_url="/login/")
def managegroup_view(request, gamename):
    groupid = query.extractGroupId(gamename)
    if not query.userIsAdminOfGroup(request.user, query.extractGroupId(gamename)):
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
            user=request.user.id, exam_id__in=relevantExams).order_by('exam')
        updatebetform = UpdateBetForm(bets=yourBets)
        betsOnYou = Bet.objects.filter(
            target=request.user.id, exam_id__in=relevantExams).order_by('exam')
        examStatsObject = query.createExamStats(betsOnYou)

        # leaderboard code groupid, name, credits query.getUserID(request.user)
        allUsersInGroup = GroupMember.objects.filter(group_id = groupid).order_by('-credits')
        infoLeaderBoard = list()
        counter = 1
        for member in allUsersInGroup:
            noOfWins = Bet.objects.filter(user_id = member.user_id, win = 1)
            oneLeaderBoard = LeaderBoardClass(counter, query.getUserName(member.user_id), member.credits, len(noOfWins))
            counter = counter + 1
            infoLeaderBoard.append(oneLeaderBoard)
        error = 'You are not the admin of this group!'
        credits = GroupMember.objects.get(group_id = groupid, user_id= query.getUserID(request.user))
        return render(request, 'game.html', {'error': error, 'admin': query.userIsAdminOfGroup(request.user, groupid), 'yourBetsList': yourBets, 'updatebetform': updatebetform, 'betForm': enterBetForm, 'betsListOnYou': examStatsObject, 'group': gamename, 'credits': credits.credits, 'leaderBoard': infoLeaderBoard})
    examlist = query.retrieveGroupExams(groupid)
    usernamelist = query.usernamesInGroup(gamename)

    # if user is not admin, redirect to gamepage
    currentUser = User.objects.get(id=request.user.id)
    if request.method == 'POST' and 'addexam' in request.POST:
        addExamForm = AddExamForm(request.POST)
        error = query.processAddExamForm(addExamForm, gamename)
        addExamForm = AddExamForm()
        addUserForm = AddUserToGroupForm()
        deleteExamForm = DeleteExamForm()
        deleteUserForm = DeleteUserForm()
        examlist = query.retrieveGroupExams(groupid)
        return render(request, 'managegroup.html', {'groupId': groupid, 'error' : error,'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm, 'examlist': examlist, 'usernamelist': usernamelist, 'deleteexam': deleteExamForm, 'deleteuser': deleteUserForm})
    elif request.method == 'POST' and 'adduser' in request.POST:
        addUserForm = AddUserToGroupForm(request.POST)
        error = query.processAddUserForm(addUserForm, gamename)
        addExamForm = AddExamForm()
        addUserForm = AddUserToGroupForm()
        deleteExamForm = DeleteExamForm()
        deleteUserForm = DeleteUserForm()
        usernamelist = query.usernamesInGroup(gamename)
        return render(request, 'managegroup.html', {'groupId': groupid, 'error' : error,'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm, 'examlist': examlist, 'usernamelist': usernamelist, 'deleteexam': deleteExamForm, 'deleteuser': deleteUserForm})
    elif request.method == 'POST' and 'removeuser' in request.POST:
        deleteUserForm = DeleteUserForm(request.POST)
        username = deleteUserForm.data['user_name']
        if str(username) == "":
            error = 'The Username field of Remove User Form cannot be empty!'
        else:
            query.removeUserFromGroup(username, gamename)
            error = False
        addExamForm = AddExamForm()
        addUserForm = AddUserToGroupForm()
        deleteExamForm = DeleteExamForm()
        deleteUserForm = DeleteUserForm()
        usernamelist = query.usernamesInGroup(gamename)
        return render(request, 'managegroup.html', {'groupId': groupid, 'error' : error,'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm, 'examlist': examlist, 'usernamelist': usernamelist, 'deleteexam': deleteExamForm, 'deleteuser': deleteUserForm})
    elif request.method == 'POST' and 'removexam' in request.POST:
        deleteExamForm = DeleteExamForm(request.POST)
        examname = deleteExamForm.data['exam_name']
        if str(examname) == "":
            error = 'The Exam Name field of Delete Exam Form cannot be empty!'
        else:
            examid = query.examNametoID(examname, gamename)
            query.removeExamFromGroup(examid, gamename)
            error = False
        addExamForm = AddExamForm()
        addUserForm = AddUserToGroupForm()
        deleteExamForm = DeleteExamForm()
        deleteUserForm = DeleteUserForm()
        examlist = query.retrieveGroupExams(groupid)
        return render(request, 'managegroup.html', {'groupId': groupid, 'error' : error,'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm, 'examlist': examlist, 'usernamelist': usernamelist, 'deleteexam': deleteExamForm, 'deleteuser': deleteUserForm})
    else:
        addExamForm = AddExamForm()
        addUserForm = AddUserToGroupForm()
        deleteExamForm = DeleteExamForm()
        deleteUserForm = DeleteUserForm()
        error = False
        return render(request, 'managegroup.html', {'groupId': groupid, 'error' : error, 'addexam': addExamForm, 'groupName': gamename, 'adduser': addUserForm, 'examlist': examlist, 'usernamelist': usernamelist, 'deleteexam': deleteExamForm, 'deleteuser': deleteUserForm})


@login_required(login_url="/login/")
def joingroup_view(request):
    if request.method == 'POST':
        return query.processJoinGroupForm(request)
    else:
        form = JoinGroupForm(request.POST)
        return render(request, 'joingroup.html', {'form': form})
