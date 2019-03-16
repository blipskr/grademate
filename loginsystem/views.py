from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from forms import RegisterForm, LoginForm, AccountEditForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

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
    return render(request, 'profile.html',)

@login_required(login_url="/login/")
def statistics_view(request):
    return render(request, 'statistics.html')

@login_required(login_url="/login/")
def accountsettings_view(request):
    if request.method == 'POST':
        form = AccountEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            password = form.cleaned_data['password1']
            editUser = authenticate(username=request.user.username, password=password)
            if editUser is not None:
                form.save()
                return redirect('/profile/')
            else:
                return render(request, 'accountsettingsautherror.html', { 'form': form, })
        else:
            return render(request, 'accountsettingswrongfielderror.html', { 'form': form })
    else:
        form = AccountEditForm(initial={'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email })
        return render(request, 'accountsettings.html', {'form': form})
