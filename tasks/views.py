from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Task, CustomUser
from .forms import CustomUserCreationForm

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