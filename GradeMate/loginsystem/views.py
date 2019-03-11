from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            return registererror_view(request, form)
    else:
        form = RegisterForm()
        return render(request, 'register.html', { 'form': form })

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
        return render(request, 'login.html', { 'form': form })

def registererror_view(request, form):
    return render(request, 'registererror.html', { 'form': form })

def loginerror_view(request, form):
    return render(request, 'loginerror.html', { 'form': form })

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login/")
def profile_view(request):
    user = request.user
    username = request.user.username
    firstname = request.user.first_name
    lastname = request.user.last_name
    email = request.user.email

    return render(request, 'profile.html', { 'username':username, 'firstname':firstname, 'lastname':lastname, 'email':email})
