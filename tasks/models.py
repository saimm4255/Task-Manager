from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Team Lead', 'Team Lead'),
        ('Member', 'Member'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')

    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_tasks')
    deadline = models.DateTimeField()
    priority = models.CharField(max_length=20, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    status = models.CharField(max_length=20, choices=[('To Do', 'To Do'), ('In Progress', 'In Progress'), ('Done', 'Done')], default='To Do')

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)

class CalendarIntegration(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    google_calendar_id = models.CharField(max_length=255)
