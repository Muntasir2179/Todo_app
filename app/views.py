from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser
from app.forms import TODOForm
from app.models import TODO

# Create your views here.


def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user)
        return render(request, 'index.html', context={'form': form, 'todos': todos})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)

    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                return redirect('home_page')
        else:
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        context = {
            "form": form
        }
        return render(request, 'signup.html', context=context)

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        if form.is_valid():
            user = form.save()
            if user is not None:
                return redirect('login_page')
        else:
            return render(request, 'signup.html', context=context)


def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect('home_page')
        else:
            return render(request, 'index.html', context={'form': form})
