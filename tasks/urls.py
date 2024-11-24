from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('tasks/', views.task_board, name='task_board'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('analytics/', views.analytics, name='analytics'),
    path('calendar/auth/', views.google_auth, name='google_auth'),
    path('calendar/callback/', views.calendar_callback, name='calendar_callback'),
    path('calendar/auth/', views.calendar_auth, name='calendar_auth'),
    path('tasks/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),


]
