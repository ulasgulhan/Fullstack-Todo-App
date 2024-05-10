from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from .serializers import (
    CompleteTaskSerializer,
    DeleteTaskSerializer,
    TaskSerializer,
    CreateTaskSerializer,
)
from .models import Task

# Create your views here.


class ShowAllTasksAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = Task.objects.all()
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)


class TaskAPIView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = Task.objects.filter(is_active=True, is_complete=False)
        active_task_count = Task.objects.filter(
            is_active=True, is_complete=False
        ).count()
        serializer = TaskSerializer(queryset, many=True)
        context = {"tasks": serializer.data, "active_task_count": active_task_count}
        return Response(context)

    def post(self, request, *args, **kwargs):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data["user_id"] = request.user.id
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, template_name=None)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteAPIView(UpdateAPIView):
    serializer_class = DeleteTaskSerializer
    queryset = Task.objects.filter(is_active=True)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        return task

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_active = False
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteAllCompletedTasksAPIView(UpdateAPIView):
    serializer_class = DeleteTaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Task.objects.filter(is_active=True, is_complete=True)
        return queryset

    def update(self, request, *args, **kwargs):
        tasks = self.get_queryset()
        for task in tasks:
            task.is_active = False
            task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCompleteAPIView(UpdateAPIView):
    serializer_class = CompleteTaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        return task

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        if task.is_complete:
            task.is_complete = False
        else:
            task.is_complete = True
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskUpdateAPIView(UpdateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        return task

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        updated_task = request.data.get("task")
        task.task = updated_task
        task.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetCompleteedTasksAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Task.objects.filter(is_active=True, is_complete=True)
        active_task_count = Task.objects.filter(
            is_active=True, is_complete=False
        ).count()
        serializer = TaskSerializer(queryset, many=True)
        context = {"tasks": serializer.data, "active_task_count": active_task_count}
        return Response(context)
