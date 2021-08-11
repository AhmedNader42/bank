from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import UserSerializer
from .models import User
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
