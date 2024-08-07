from django.contrib import admin
from django.urls import path
from tasks import views
from django.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_or_register, name='login_or_register'),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.tasks, name='tasks'),
    path('tasks_completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete', views.delete_task, name='delete_task'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('register/', views.register, name='register'),
    
    # Password reset 
    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password'),
    path('reset_password/', views.password_reset_request, name='reset_password'),
    # Email sent
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name='password_reset_done'),
    # Reset password form url
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    # Password reset complete
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),

    # path('accounts/', include('allauth.urls')),
]
