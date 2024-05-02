from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .serializers import TaskSerializer
from .models import Task

# Create your views here.

class TaskListAPIView(ListAPIView):
    queryset = Task.objects.filter(is_active=True)
    serializer_class = TaskSerializer