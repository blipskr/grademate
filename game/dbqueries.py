from django.contrib.auth.models import User
from forms import EnterBetForm, UpdateBetForm, EnterMarksForm, JoinGroupForm
from models import Result, Exam, GroupMember, Bet, Group
from ExamStats import ExamStats
import math
import unicodedata
from django.shortcuts import render, render_to_response, redirect
import views as v

# method takes as an input request
# returns a list of current users groups

def calculateWinner(userid, examid, finalscore, groupname):
    groupid = extractGroupId(groupname)
    groupObject = Group.objects.get(pk=groupid)
    examObject = Exam.objects.get(exam_id=examid)
    userObject = User.objects.get(pk=userid)
    listOfBets = Bet.objects.filter(target=userObject, exam=examObject)
    print "number of bets is " + str(listOfBets.count())
    if listOfBets.count() == 0:
        return
    closestguess = 100
    finalscore = int(finalscore)
    # find closest guess
    for bet in listOfBets:
        if abs(finalscore - bet.guess_mark) < closestguess:
            closestguess = abs(finalscore - bet.guess_mark)
    print "closest guess is " + str(closestguess)
    # find average bet ammount on user+exam
    averageAmmount = averageBetOnUserExam(userObject, examObject)
    print "average ammount on user+Exam is " + str(averageAmmount)
    # iterate through all users and make them winners/losers
    for bet in listOfBets:
        # if it is winner
        if abs(finalscore - bet.guess_mark) == closestguess:
            # set the bet as win
            bet.win = True
            bet.save()
        # if it is loser
        elif abs(finalscore - bet.guess_mark) > closestguess:
            bet.win = False
            bet.save()
    print "set winners and losers"
    # list of win bets
    listOfWinBets = listOfBets.exclude(win=False)
    # calculate number of winners
    noOfWinners = listOfWinBets.count()
    # credits from pot of each winner
    eachWinsCredits = math.trunc(float(sumBetOnUserExam(userObject, examObject)) / noOfWinners)
    # reward all winners
    print "starting to reward winners with credits"
    for bet in listOfWinBets:
        # get the winner
        userObjectFromBet = bet.user
        groupMemberObjectFromBet = GroupMember.objects.get(group = groupObject, user=userObjectFromBet)
        # get winners current credits
        oldCredits = groupMemberObjectFromBet.credits
        # get credits to add
        multiplier = calculateMultiplier(averageAmmount, bet.guess_credits)
        addCredits = multiplier * eachWinsCredits
        # calculate new credits and update them
        newCredits = oldCredits + addCredits
        groupMemberObjectFromBet.credits = newCredits
        groupMemberObjectFromBet.save()
        print str(groupMemberObjectFromBet.user)
    print "rewarded winners with credits"

def retrieveUsersGroups(request):
    usersGroups = GroupMember.objects.filter(user=request.user.id)
    return usersGroups

# method takes as an input array of Bet objects
# returns a list of ExamStats objects, each of which contains
# average bet and no of ExamStats
# on current user for each exam


def examIDtoName(examid):
    examObject = Exam.objects.get(pk=examid)
    examName = examObject.exam_name
    return examName

def examNametoID(examname, groupname):
    groupObject = Group.objects.get(group_name=groupname)
    examObject = Exam.objects.get(exam_name=examname)
    return examObject.exam_id

def createExamStats(betsObject):
    examStatsObject = []
    tempId = 0
    # create an ExamStats object for each Bet object
    for element in betsObject:
        exam_name = examIDtoName(element.exam_id)
        examStatsTemp = ExamStats(
            id=tempId, exam_id=element.exam_id, average_bet=element.guess_mark, no_of_bets=1, exam_name=exam_name)
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
# method takes request and betForm, processes betForm


def processJoinGroupForm(request):
    form = JoinGroupForm(request.POST)
    group_name = form.data['group_name']
    group_id = form.data['group_id']
    try:
        group = Group.objects.get(pk=group_id)
        if (GroupMember.objects.filter(user=request.user, group=group).count() == 0):
            if (int(extractGroupId(group_name)) == int(group_id)):
                newGroupMember = GroupMember(
                    group=group, user=request.user, credits=100)
                newGroupMember.save()
                return redirect('/game/' + group_name)
            else:
                return render(request, 'groupnotfounderror.html', {'form': form})
        else:
            return render(request, 'alreadyingrouperror.html', {'form': form})
    except:
        return render(request, 'groupnotfounderror.html', {'form': form})


def processEnterMarksForm(request, enterMarksForm, gamename):
    groupid = extractGroupId(gamename)
    groupExamIds = examIDsinGroup(gamename)
    userResults = Result.objects.filter(
        user=request.user.id, exam_id__in=groupExamIds)
    examname = enterMarksForm.data['exam']
    enteredMark = enterMarksForm.data['mark']
    if str(examname) == "":
        return render(request, 'invalidexam.html', {'EnterMarksForm': EnterMarksForm(group=groupid), 'group': gamename, 'userResultsList': userResults})
    elif str(enteredMark) == "":
        return render(request, 'invalidmark.html', {'EnterMarksForm': EnterMarksForm(group=groupid), 'group': gamename, 'userResultsList': userResults})
    examid = extractExamIDgivenGroup(examname, gamename)
    alreadyEnteredExams = []
    for result in userResults.values():
        alreadyEnteredExams.append(result['exam_id'])
    if examid in alreadyEnteredExams:
        return render(request, 'duplicateresultentry.html', {'EnterMarksForm': EnterMarksForm(group=groupid), 'group': gamename, 'userResultsList': userResults})
    exam = Exam.objects.get(pk=examid)
    if not (int(enteredMark) >= 0 and int(enteredMark) <= 100):
        return render(request, 'invalidmark.html', {'EnterMarksForm': EnterMarksForm(group=groupid), 'group': gamename, 'userResultsList': userResults})
    else:
        newResult = Result(exam=exam, user=request.user, mark=enteredMark)
        newResult.save()
        calculateWinner(request.user.id, examid, enteredMark, gamename)
        return redirect('/game/' + gamename + '/entermarks/')


def usernamesInGroup(groupName):
    groupId = Group.objects.get(group_name=groupName).group_id
    groupMemberObjects = GroupMember.objects.filter(
        group=groupId).values('user_id')
    usernameList = []
    for groupObject in groupMemberObjects:
        uid = groupObject['user_id']
        user = User.objects.get(pk=uid)
        username = user.username

        usernameList.append(username)
    return usernameList


def processEnterBetForm(request, betForm, gamename):
    user = request.user
    targetname = betForm.data['target']
    examname = betForm.data['exam']
    guessmark = betForm.data['guess_mark']
    guesscredits =  betForm.data['guess_credits']
    try:
        int(guessmark)
    except:
        return "Your prediction must be a whole number from 0 to 100."
    try:
        int(guesscredits)
    except:
        return "You cannot use decimal credits."
    if (str(targetname) == "" or str(examname) == "" or str(guessmark) == "" or str(guesscredits) == ""):
        return 'Make sure you have chosen an exam, a target,a mark and an amount of credits!'
    examid = extractExamIDgivenGroup(examname, gamename)
    targetid = getUserID(targetname)
    if not (int(guessmark) >= 0 and int(guessmark) <= 100):
        return 'Predicted mark invalid. Make sure it is between 0 and 100!'
    groupid = extractGroupId(gamename)
    credits = GroupMember.objects.get(group_id = groupid, user_id= getUserID(user))
    if int(credits.credits) < int(guesscredits):
        return 'You do not have enough credits.'
    elif int(guesscredits) <= 0:
        return 'You must use at least 1 credit.'
    exam = Exam.objects.get(pk=examid)
    target = User.objects.get(pk=targetid)
    if Bet.objects.filter(user=user, target=target, exam=exam).count() != 0:
        return 'You have aleady made a bet on that user for this exam.'
    newBet = Bet(exam=exam, user=request.user,
                 target=target, guess_mark=guessmark, guess_credits = guesscredits)
    groupid = extractGroupId(gamename)
    credits = GroupMember.objects.get(group_id = groupid, user_id= getUserID(user))
    if int(credits.credits) < int(guesscredits):
        return 'Not enough credits!'
    elif int(guesscredits) <= 0:
        return 'Minimum amount of credits to bet is 1!'

    newBet.save()
    credits.credits = int(credits.credits) - int(guesscredits)
    credits.save()
    return False
# method takes request and betForm, processes UpdateBetForm


def processUpdateBetForm(request, betForm):
    newmark = betForm.data['mark']
    betid = betForm.data['bet']
    if str(newmark) == "" or str(betid) == "":
        return 'The User and New Mark fields of Change Prediction Form cannot be left empty!'
    betObject = Bet.objects.get(pk=betid)
    try:
        int(newmark)
    except:
        return "Your new prediction must be a whole number from 0 to 100."

    if not (int(newmark) >= 0 and int(newmark) <= 100):
        return 'The New Mark entered is invalid!'
    Bet.objects.filter(pk=betid).update(guess_mark=newmark)
    return False

def processAddExamForm(addExamForm, gamename):
    exam_name = addExamForm.data['exam_name']
    if str(exam_name) == "":
        return 'The Exam Name field in the Add Exam Form must not be empty'
    else:
        createNewExam(exam_name, gamename)
        return False

def processAddUserForm(addUserForm, gamename):
    user_name = addUserForm.data['user_name']
    if str(user_name) == "":
        return "The Username Field of Add User Form cannot be left empty!"
    elif not User.objects.filter(username=user_name):
        return "The user you tried to add does not exist!"
    else:
        addUserToGroup(user_name, gamename)
        return False


# Returns list of user's group IDs which he is a member of.
def retrieveUserGroupIds(userId):
    userGroupsObject = GroupMember.objects.filter(
        user=userId).values('group_id')
    userGroupIdsList = []
    for element in userGroupsObject:
        groupId = element['group_id']
        userGroupIdsList.append(groupId)
    return userGroupIdsList

# Takes a list of groupIds and returns a list of corresponding groupnames


def extractGroupNames(groupIds):
    listOfGroupNames = []
    for groupId in groupIds:
        groupObject = Group.objects.filter(
            group_id=groupId).values('group_name')
        groupName = groupObject[0]['group_name']
        listOfGroupNames.append(groupName)
    return listOfGroupNames

# takes a name of group and returns its id


def extractGroupId(groupName):
    try:
        groupObject = Group.objects.get(group_name=groupName)
        groupId = groupObject.group_id
        return groupId
    except Group.DoesNotExist:
        return None


def getUserID(targetname):
    userObject = User.objects.get(username=targetname)
    userID = userObject.id
    return userID

def getUserName(targetid):
    userObject = User.objects.get(id = targetid)
    userName = userObject.username
    return userName


def extractExamIDgivenGroup(examname, gamename):
    groupid = extractGroupId(gamename)
    examObject = Exam.objects.get(exam_name=examname, group_id=groupid)
    examid = examObject.exam_id
    return examid

# takes an id of a group ans returns its name


def extractGroupName(groupId):
    groupObject = Group.objects.get(group_id=groupId)
    groupName = groupObject.group_name
    return groupName

# takes an id of a group and returns all the exam names associated with the group


def retrieveGroupExams(groupId):
    examObjects = Exam.objects.filter(group=groupId).values('exam_name')
    listOfExamNames = []
    for examObject in examObjects:
        examName = examObject['exam_name']
        listOfExamNames.append(examName)
    return listOfExamNames


def getGroups(request):
    userId = request.user.id
    groups = extractGroupNames(retrieveUserGroupIds(userId))
    return groups

# Takes a name of the group and returns list of tuples containing userIds and usernames respectively


def userIDsinGroup(groupName):
    groupId = Group.objects.get(group_name=groupName).group_id
    groupMemberObjects = GroupMember.objects.filter(
        group=groupId).values('user_id')
    userIdsList = []
    for groupObject in groupMemberObjects:
        userId = groupObject['user_id']
        uid = User.objects.get(pk=userId)
        userIdsList.append(userId)
    return userIdsList

# Takes a name of group and returns all esxams associated with it


def examIDsinGroup(groupName):
    groupId = Group.objects.get(group_name=groupName).group_id
    examObjects = Exam.objects.filter(group=groupId).values('exam_id')
    examIDsList = []
    for groupObject in examObjects:
        examID = groupObject['exam_id']
        examIDsList.append(examID)
    return examIDsList

# Creates a new group with given name


def createNewGroup(username, groupName):
    try:
        examObject = Group.objects.get(exam_name=groupName)
    except:
        groupObject = Group(group_name=groupName)
        groupObject.save()
        addUserToGroup(username, groupName)

# creates new exam with given name for given group


def createNewExam(examName, groupName):
    groupObject = Group.objects.get(group_name=groupName)
    examObject = Exam(group=groupObject, exam_name=examName)
    examObject.save()

# adds given user to the given group by name


def addUserToGroup(user_name, groupName):
    try:
        userObject = User.objects.get(username=user_name)
        groupObject = Group.objects.get(group_name=groupName)
        groupMemberObject = GroupMember.objects.get(
            user=userObject, group=groupObject)
    # if GroupMember does not exist, create it
    except:
        groupObject = Group.objects.get(group_name=groupName)
        userObject = User.objects.get(username=user_name)
        groupMemberObject = GroupMember(
            group=groupObject, user=userObject, credits=100)
        groupMemberObject.save()

# method to delete user from the group


def removeUserFromGroup(userName, groupName):
    # determine groupObject, userObject, betObjects, resultObjects, groupMemberObject
    userObject = User.objects.get(username=userName)
    groupObject = Group.objects.get(group_name=groupName)
    groupMemberObject = GroupMember.objects.get(
        group=groupObject, user=userObject)
    betObjects1 = Bet.objects.filter(target=userObject)
    betObjects2 = Bet.objects.filter(user=userObject)
    # delete it
    groupMemberObject.delete()
    betObjects1.delete()
    betObjects2.delete()

# method to delete exam from the group


def removeExamFromGroup(examid, groupName):
    # determine groupObject, examObject, betObjects and resultObjects
    groupObject = Group.objects.get(group_name=groupName)
    examObject = Exam.objects.get(exam_id=examid, group=groupObject)
    betObjects = Bet.objects.filter(exam=examObject)
    resultObjects = Result.objects.filter(exam=examObject)
    # delete it
    betObjects.delete()
    examObject.delete()
    resultObjects.delete()

# method to check if given user is creator (admin) of the group
# returns true if he is


def userIsAdminOfGroup(userObject, groupid):
    #userObject = User.objects.get(username = userName)
    groupObject = Group.objects.get(pk=groupid)
    groupMemberObjects = GroupMember.objects.filter(group=groupObject)
    groupAdminObject = groupMemberObjects[0]
    groupMemberObject = GroupMember.objects.get(
        group=groupObject, user=userObject)
    if groupAdminObject == groupMemberObject:
        return True
    else:
        return False

# method to check if given user is a member of given group


def userIsMemberOfGroup(userName, groupName):
    userObject = User.objects.get(username=userName)
    groupObject = Group.objects.get(group_name=groupName)
    try:
        groupMemberObject = GroupMember.objects.get(
            group=groupObject, user=userObject)
        return True
    except GroupMember.DoesNotExist:
        return False


def fetchUserExamsInGroup(username, groupname):
    userObject = User.objects.get(username=username)
    groupObject = Group.objects.get(group_name=groupname)
    exams = Exam.objects.filter(group=groupObject)
    return exams

# function for changing ammount of users credits
def changeUserCredits(username, groupname, ammount):
    groupObject = Group.objects.get(group_name = groupname)
    userObject = User.objects.get(username = username)
    groupMemberObject = GroupMember.objects.get(group = groupObject, user = userObject)
    currentCredits = groupMemberObject.credits
    newCredits = currentCredits + ammount
    GroupMember.objects.get(group = groupObject, user = userObject).update(credits = newCredits)

# function for calculating average bet on GroupMember + Exam
def averageBetOnUserExam(userObject, examObject):
    sum = 0
    number = 0
    betsObjects = Bet.objects.filter(target = userObject, exam = examObject)
    for bet in betsObjects:
        sum += bet.guess_credits
        number += 1
    average = math.trunc(float(sum) / number)
    return average

# function for calculating pot on the user+exam
def sumBetOnUserExam(userObject, examObject):
    sum = 0
    betsObjects = Bet.objects.filter(target = userObject, exam = examObject)
    for bet in betsObjects:
        sum += bet.guess_credits
    return sum

# function for calculating multiplier given guess mark and exam mark
# this function is used when rewarding winners
def calculateMultiplier(average, actual):
    return float(actual) / average

# function for calculating difference of given bet from real mark
# given bet object and result object
def calculateDifferenceFromMark(bet, result):
    return abs(bet.guess_mark - result.mark)
