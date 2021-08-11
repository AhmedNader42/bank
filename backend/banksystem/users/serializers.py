from rest_framework import serializers
from .models import User
from rest_framework.permissions import IsAdminUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'user_type')
