from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.TaskListAPIView.as_view(template_name='index.html'), name='task-list'),
    path('tasks/create', views.TaskCrateAPIView.as_view(), name='task-create'),
    path('tasks/delete/<int:id>', views.TaskDeleteAPIView.as_view(), name='task-delete'),
    path('tasks/complete/<int:id>', views.TaskCompleteAPIView.as_view(), name='task-complete'),
]