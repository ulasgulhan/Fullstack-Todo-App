from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from .serializers import CompleteTaskSerializer, DeleteTaskSerializer, TaskSerializer, CreateTaskSerializer
from .models import Task

# Create your views here.

class TaskListAPIView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(is_active=True)
        serializer = TaskSerializer(tasks, many=True)
        context['tasks'] = serializer.data
        return context


class TaskCrateAPIView(CreateAPIView):
    serializer_class = CreateTaskSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteAPIView(UpdateAPIView):
    serializer_class = DeleteTaskSerializer

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)
        return task
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_active = False
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)


class TaskCompleteAPIView(UpdateAPIView):
    serializer_class = CompleteTaskSerializer

    def get_object(self):
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)
        return task
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_complete = True
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)
    