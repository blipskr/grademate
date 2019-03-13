from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login/")
def creategroup_view(request):
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
