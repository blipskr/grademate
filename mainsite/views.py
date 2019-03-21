from django.shortcuts import render, render_to_response
from game import dbqueries as query
# Create your views here.


def index(request):
    return render(request, 'index.html')


def agreement(request):
    return render(request, 'agreement.html')


def mygroups(request):
    groups = query.retrieveUsersGroups(request)
    return render(request, 'mygroups.html', {'groups': groups})


def test(request):
    return render(request, 'test.html')
