from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        chenck_username = User.objects.filter(username=validated_data["username"])
        if chenck_username:
            return False
        else:
            user = User.objects.create(
                username=validated_data["username"], email=validated_data["email"]
            )
            user.set_password(validated_data["password"])
            user.save()
            return user
