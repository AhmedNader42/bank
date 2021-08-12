from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import CustomUserDetailsSerializer as UserSerializer
from .models import User
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdminUser, )
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, pk=None):
        if not request.user.is_superuser:
            raise PermissionDenied
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        if user != request.user and not request.user.is_superuser:
            raise PermissionDenied
        serializer = UserSerializer(user)
        return Response(serializer.data)
