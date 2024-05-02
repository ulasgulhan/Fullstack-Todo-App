from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from .serializers import CompleteTaskSerializer, DeleteTaskSerializer, TaskSerializer, CreateTaskSerializer
from .models import Task

# Create your views here.

class TaskAPIView(APIView):
    queryset = Task.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = Task.objects.filter(is_active=True)
        serializer = TaskSerializer(queryset, many=True)
        context = {'tasks': serializer.data}
        return render(request, 'index.html', context)
    
    def post(self, request, *args, **kwargs):
        serializer = CreateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDeleteAPIView(UpdateAPIView):
    serializer_class = DeleteTaskSerializer
    queryset = Task.objects.filter(is_active=True)
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        task_id = self.kwargs.get('id')
        task = Task.objects.get(id=task_id)
        return task
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_active = False
        task.save()
        serializer = self.get_serializer(task)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCompleteAPIView(UpdateAPIView):
    serializer_class = CompleteTaskSerializer
    queryset = Task.objects.filter(is_active=True)
    permission_classes = (permissions.AllowAny,)

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
    