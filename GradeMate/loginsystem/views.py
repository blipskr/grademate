from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from forms import RegisterForm, LoginForm

# Create your views here.
def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def register2(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            return redirect('/register2/')
    else:
        form = RegisterForm()
        return render(request, 'register2.html', { 'form': form })

def login2(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            return redirect('/')
        else:
            return redirect('/login2/')
    else:
        form = LoginForm()
        return render(request, 'login2.html', { 'form': form })
