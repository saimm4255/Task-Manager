from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Task, CustomUser
from .forms import CustomUserCreationForm
from google_auth_oauthlib.flow import Flow
from django.http import HttpResponse
import os
from django.contrib.auth.decorators import user_passes_test

@login_required
def task_board(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'task_board.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to_id = request.POST['assigned_to']
        deadline = request.POST['deadline']
        priority = request.POST['priority']
        assigned_to = CustomUser.objects.get(id=assigned_to_id)
        Task.objects.create(
            title=title, description=description, assigned_to=assigned_to,
            created_by=request.user, deadline=deadline, priority=priority
        )
        return redirect('task_board')
    users = CustomUser.objects.all()
    return render(request, 'create_task.html', {'users': users})




@login_required
def analytics(request):
    task_count = Task.objects.filter(assigned_to=request.user).count()
    completed_tasks = Task.objects.filter(assigned_to=request.user, status='Done').count()
    return render(request, 'analytics.html', {
        'task_count': task_count,
        'completed_tasks': completed_tasks,
    })

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})



def google_auth(request):
    flow = Flow.from_client_secrets_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=request.build_absolute_uri('/calendar/callback/')
    )
    authorization_url, _ = flow.authorization_url(prompt='consent')
    request.session['flow'] = flow
    return redirect(authorization_url)    



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' 
GOOGLE_CLIENT_ID = 'your_google_client_id.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'your_google_client_secret'
REDIRECT_URI = 'http://localhost:8000/calendar/callback/'  

SCOPES = ['https://www.googleapis.com/auth/calendar']

flow = Flow.from_client_config(
    {
        "web": {
            "client_id": GOOGLE_CLIENT_ID,
            "project_id": "your_project_id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uris": [REDIRECT_URI],
        }
    },
    scopes=SCOPES,
)

def calendar_callback(request):
    """Handles Google OAuth2 callback and saves credentials."""
    flow.redirect_uri = REDIRECT_URI
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials



    return HttpResponse("Google Calendar integration successful!")

def calendar_auth(request):
    """Redirects user to Google OAuth consent screen."""
    flow.redirect_uri = REDIRECT_URI
    authorization_url, _ = flow.authorization_url(prompt='consent')
    return redirect(authorization_url)


@login_required
def update_task_status(request, task_id):
    task = Task.objects.get(id=task_id, assigned_to=request.user)
    new_status = request.POST['status']
    task.status = new_status
    task.save()
    return JsonResponse({'success': True})



def is_admin(user):
    return user.role == 'Admin'

@user_passes_test(is_admin)
def admin_dashboard(request):
  
    pass
