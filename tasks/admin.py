from django.contrib import admin
from .models import CustomUser, Task, Notification, CalendarIntegration

admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Notification)
admin.site.register(CalendarIntegration)
