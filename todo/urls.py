from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListAPIView.as_view(), name='task_list'),
]