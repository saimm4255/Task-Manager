from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.task_board, name='task_board'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('analytics/', views.analytics, name='analytics'),
]
