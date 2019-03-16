from django.shortcuts import render, render_to_response
from game import dbqueries as query
# Create your views here.
def index(request):
    return render(request, 'index.html')

def agreement(request):
    return render(request, 'agreement.html')

def mygroups(request):
    return render(request, 'mygroups.html', { 'groupIDs': query.retrieveUserGroupIds(request.user.id), 'groupNames': query.getGroups(request) })
