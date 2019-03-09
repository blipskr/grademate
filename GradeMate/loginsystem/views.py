from django.shortcuts import render, render_to_response

# Create your views here.
def login(request):
    return render_to_response('login.html')

def register(request):
    return render_to_response('register.html')
