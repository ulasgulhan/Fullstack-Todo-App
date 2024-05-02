from django.db import models

# Create your models here.


class Task(models.Model):
    task        = models.CharField(max_length=300)
    is_complete = models.BooleanField(default=False)
    is_active   = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
