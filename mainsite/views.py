from django.shortcuts import render, render_to_response

# Create your views here.
def index(request):
    return render(request, 'index.html')

def agreement(request):
    return render(request, 'agreement.html')

def mygroups(request):
    return render(request, 'mygroups.html')
