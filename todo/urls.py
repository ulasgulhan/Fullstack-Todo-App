from django.urls import path
from . import views


urlpatterns = [
    path("tasks/", views.ShowAllTasksAPIView.as_view(), name="task"),
    path("tasks/active", views.TaskAPIView.as_view(), name="task-list"),
    path("tasks/create", views.TaskAPIView.as_view(), name="task-create"),
    path(
        "tasks/delete/<int:task_id>",
        views.TaskDeleteAPIView.as_view(),
        name="task-delete",
    ),
    path(
        "tasks/complete/<int:task_id>",
        views.TaskCompleteAPIView.as_view(),
        name="task-complete",
    ),
    path(
        "tasks/update/<int:task_id>",
        views.TaskUpdateAPIView.as_view(),
        name="task-update",
    ),
    path(
        "tasks/completed/",
        views.GetCompleteedTasksAPIView.as_view(),
        name="task-list-complete",
    ),
    path(
        "tasks/completed/delete-all",
        views.DeleteAllCompletedTasksAPIView.as_view(),
        name="task-complete-delete",
    ),
]
