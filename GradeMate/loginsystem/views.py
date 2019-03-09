from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from forms import RegisterForm, LoginForm
from django.contrib.auth import login

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return redirect('/register/')
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
            return redirect('/login/')
    else:
        form = LoginForm()
        return render(request, 'login.html', { 'form': form })
