from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.urls import include
# Imports related to email reset password diy
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.html import strip_tags
from allauth.socialaccount.models import SocialApp, SocialAccount, SocialToken

def login_or_register(request):
    context = {"providers": SocialApp.objects.all()}

    if request.method == 'POST':
        # Registration form submission
        if 'password1' in request.POST and 'password2' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            # Ensure all fields are filled
            if not (username and email and password1 and password2):
                context['register_error'] = 'Please fill all missing blanks.'
                return render(request, 'login.html', context)

            # Check if passwords match
            if password1 != password2:
                context['register_error'] = 'Password must match its confirmation.'
                return render(request, 'login.html', context)

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                context['register_error'] = 'Email already exists.'
                return render(request, 'login.html', context)

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                context['register_error'] = 'Username already exists.'
                return render(request, 'login.html', context)

            try:
                # Create a new user
                user = User.objects.create_user(username=username, email=email, password=password1)
                # Login the new user
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                context['register_error'] = 'User already exists.'
                return render(request, 'login.html', context)

        # Login form submission
        elif 'username_or_email' in request.POST and 'password' in request.POST:
            username_or_email = request.POST.get('username_or_email')
            password = request.POST.get('password')

            # Ensure both username/email and password are provided
            if not username_or_email or not password:
                context['login_error'] = 'Username or password is missing.'
                return render(request, 'login.html', context)

            # Authenticate the user with username or email
            user = authenticate(request, username=username_or_email, password=password) or \
                   authenticate(request, email=username_or_email, password=password)
            if user is None:
                context['login_error'] = 'Wrong credentials, try again.'
                return render(request, 'login.html', context)
            # Login the authenticated user
            login(request, user)
            return redirect('tasks')

    elif request.method == 'GET':
        # Render the login form
        return render(request, 'login.html', context)

    # Handle invalid requests
    context['error'] = 'Invalid request.'
    return render(request, 'login.html', context)

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
        print(f'Task {task_id} marked as completed at {task.dateCompleted}')
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
    
def password_reset_request(request):
    if request.method == 'POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            data = password_form.cleaned_data['email']
            user_email = User.objects.filter(email=data)
            if user_email.exists():
                for user in user_email:
                    subject = 'Password Reset Request'
                    email_template_name = 'password_reset_email.html'
                    parameters = {
                        'user': user,  # Pass the user object directly
                        'domain': 'task-hive.azurewebsites.net',
                        'site_name': 'TaskHive',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'protocol': 'https',
                    }
                    html_message = render_to_string(email_template_name, parameters)
                    plain_message = strip_tags(html_message)
                    try:
                        # Send email with HTML and plain text versions
                        send_mail(subject, plain_message, 'admin@TaskHive.com', [user.email], html_message=html_message)
                    except BadHeaderError:
                        return HttpResponse("Invalid header.")
                    return redirect('password_reset_done')
    else:
        password_form = PasswordResetForm()
    context = {
        'password_form': password_form,
    }
    return render(request, 'password_reset.html', context)