from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import include

def login_or_register(request):
    if request.method == 'POST':
        # Registration form submission
        if 'password1' in request.POST and 'password2' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Ensure all fields are filled
            if not (username and email and password1 and password2):
                return render(request, 'login.html', {'register_error': 'Please fill all missing blanks.'})

            # Check if passwords match
            if password1 != password2:
                return render(request, 'login.html', {'register_error': 'Password must match its confirmation.'})

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                return render(request, 'login.html', {'register_error': 'Email already exists.'})

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return render(request, 'login.html', {'register_error': 'Username already exists.'})

            try:
                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password1)
                # Login the new user
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'login.html', {'register_error': 'User already exists.'})

        # Login form submission
        elif 'username_or_email' in request.POST and 'password' in request.POST:
            username_or_email = request.POST.get('username_or_email')
            password = request.POST.get('password')

            # Ensure both username/email and password are provided
            if not username_or_email or not password:
                return render(request, 'login.html', {'login_error': 'Username or password is missing.'})

            # Authenticate the user with username or email
            user = authenticate(request, username=username_or_email, password=password) or \
                   authenticate(request, email=username_or_email, password=password)
            if user is None:
                return render(request, 'login.html', {'login_error': 'Wrong credentials, try again.'})
            # Login the authenticated user
            login(request, user)
            return redirect('tasks')

    elif request.method == 'GET':
        # Render the login form
        return render(request, 'login.html')

    # Handle invalid requests
    return render(request, 'login.html', {'error': 'Invalid request.'})

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
