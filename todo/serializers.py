from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['user_id', 'task']
    
    def save(self):
        task = Task.objects.create(
            user_id = self.validated_data['user_id'],
            task = self.validated_data['task']
        )

        task.save()
        return task

class DeleteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_active']


class CompleteTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['is_complete']