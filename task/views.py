from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {'form': UserCreationForm()})
    else:
        try:
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('tasks')
        except IntegrityError:
            return render(request, 'signup.html', {
                'form': UserCreationForm(),
                'error': "El usuario ya existe"
            })
        else:
            return render(request, "signup.html", {'form': form})

def tasks(request):
    return render(request, 'tasks.html')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == "GET":
        return render(request, 'login.html', {'form': AuthenticationForm()})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'login.html', {'form': form, 'error': "Credenciales inválidas"})
