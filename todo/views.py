from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from .serializers import CompleteTaskSerializer, DeleteTaskSerializer, TaskSerializer, CreateTaskSerializer
from .models import Task

# Create your views here.

class TaskAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(is_active=True)
        serializer = TaskSerializer(tasks, many=True)
        context = {'tasks': serializer.data}
        return render(request, 'index.html', context)
    
    def post(self, request, *args, **kwargs):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = self.get()
            return Response(context, status=status.HTTP_201_CREATED)
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
    