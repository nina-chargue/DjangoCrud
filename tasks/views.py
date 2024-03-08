from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def login_or_register(request):
    if request.method == 'POST':
        print(request.POST)
        if 'password1' in request.POST and 'password2' in request.POST:
            print("This is a registration attempt")
            if request.POST['password1'] == request.POST['password2']:
                print("Passwords Match")
                try:
                    print(request.POST['username'])
                    print(request.POST['password1'])
                    print(User.objects)
                    user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                    print("Registration of user successful!")
                    user.save()
                    print("User saved in the DB")
                    login(request, user)
                    print("Login successful!")
                    return redirect('tasks')
                except IntegrityError:
                    print("User already exists")
                    return render(request, 'login.html', {
                        'error': 'User already exists'
                    })
            else:
                print("Password does not match")
                return render(request, 'login.html', {
                    'error': 'Password does not match'
                })
        else:
            print("This is a login attempt")
            user = authenticate(
                request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                print("Username or password is incorrect.")
                return render(request, 'login.html', {
                    'error': 'Username or password is incorrect.'
                })
            login(request, user)
            print("Login successful..")
            return redirect('tasks')
                
    elif request.method == 'GET':
        return render(request, 'login.html')

# def login(request):
#     if request.method == 'POST':
#         # Handle sign-in logic
#         user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
#         if user is not None:
#             login(request, user)
#             print("Login successful..")
#             return redirect('tasks')
#         else:
#             print("Username or password is incorrect.")
#             return render(request, 'login.html', {
#                 'error': 'Username or password is incorrect.'
#             })
#     elif request.method == 'GET':
#         return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                print("User already exists")
                return render(request, 'login.html', {
                    'error': 'User already exists'
                })
        else:
            print("Password does not match")
            return render(request, 'login.html', {
                'error': 'Password does not match'
            })
    elif request.method == 'GET':
        return render(request, 'login.html')

def home(request):
    print("corriendo home")
    return render (request, 'home.html')

def signup(request):
    if request.method == 'GET':
        # return render(request, 'signup.html', {
        #     'form': UserCreationForm
        # })
        return render(request, 'login.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            print("Passwords Match")
            # Register user
            try:
                print(request.POST['username'])
                print(request.POST['password1'])
                print(User.objects)
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                print("Registration of user successful!")
                user.save()
                print("User saved in the DB")
                login(request, user)
                print("Login successful!")
                return redirect('tasks')
            except IntegrityError:
                print("User already exists")
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        print("Password does not match")
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Password does not match'
        })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, dateCompleted__isnull=False).order_by('-dateCompleted')
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render (request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'create_task.html', {
            'form': TaskForm,
            'error': 'Please provide valid data'
        })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': 'Error updating task.'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.dateCompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    
@login_required
def signout(request):
    logout(request)
    return redirect('login_or_register')

def signin(request):
    if request.method == 'GET':
        # return render(request, 'signin.html', {"form": AuthenticationForm})
        return render(request, 'login.html')
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks')

        
    
