from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser, logout
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url='login_page')
# forcing user to login first and denying the access of any other link without being logged in
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user=user).order_by('priority')
        return render(request, 'index.html', context={'form': form, 'todos': todos})


def login(request):
    if request.method == 'GET':
        # When user wants to login
        # AuthenticationForm() is a build in class to create registration/signup form
        form = AuthenticationForm()
        context = {
            "form": form
        }
        return render(request, 'login.html', context=context)

    else:
        # when user has logged in
        form = AuthenticationForm(data=request.POST)
        # checking if the user entered correct credentials
        if form.is_valid():
            # fetching data from the FORM
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # checking if the entered credentials matches with the database credentials
            user = authenticate(username=username, password=password)
            if user is not None:
                loginUser(request, user)
                # if user is successfully logged in then serve him the home page
                # calling the home function using urls.py
                return redirect('home_page')
        else:
            # if user entered wrong credentials then serving him the same login page to enter correct credentials
            context = {
                "form": form
            }
            return render(request, 'login.html', context=context)


def signup(request):
    # if user clicked signup then the request would be 'GET'
    if request.method == 'GET':
        # creating a form using the build in UserCreationForm() class
        form = UserCreationForm()
        context = {
            "form": form
        }
        # returning the signup form to user
        return render(request, 'signup.html', context=context)

    # if user clicked signup then the request would be 'POST' and user must have entered some data
    if request.method == 'POST':
        # Creating a form with the users entered data
        form = UserCreationForm(request.POST)
        context = {
            "form": form
        }
        # checking if the user has entered the corrected data or not
        if form.is_valid():
            # user entered the correct information and signup is done and saving the data into the database
            user = form.save()
            if user is not None:
                # as the registration is done, sending the user to the login page
                return redirect('login_page')
        else:
            # if user doesn't entered the correct information then keep the user on the same page
            return render(request, 'signup.html', context=context)


def add_todo(request):
    # checking if the user is logged in or not
    if request.user.is_authenticated:
        # saving the users information into user variable
        user = request.user
        # creating a TODOForm with the users entered information
        form = TODOForm(request.POST)
        if form.is_valid():
            # save the information temporarily
            todo = form.save(commit=False)
            # assigning the user with the data he entered so that we can know which user entered that data
            todo.user = user
            # saving the user entered information permanently
            todo.save()
            # returning user to the home page through urls.py
            return redirect('home_page')
        else:
            # if user entered wrong data in the add-todo form then present user the same page and as for correct data
            return render(request, 'index.html', context={'form': form})


def signout(request):
    # using build in logout function
    logout(request)
    return redirect('login_page')


def delete_todo(request, id):
    # taking id as the parameter of the function
    # the following query deletes the information with the id that has passed with the function
    TODO.objects.get(pk=id).delete()
    # returning to the home page
    return redirect('home_page')


def change_todo(request, id, status):
    # getting id and status as parameters
    # the following query finds the information that has the id
    todo = TODO.objects.get(pk=id)
    # updating the status of that particular information
    todo.status = status
    # saving the data into the database
    todo.save()
    return redirect('home_page')
