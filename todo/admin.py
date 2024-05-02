from django.contrib import admin
from .models import Task

# Register your models here.


class TasksAdmin(admin.ModelAdmin):
    list_display    = ('task', 'is_complete', 'is_active')


admin.site.register(Task, TasksAdmin)
