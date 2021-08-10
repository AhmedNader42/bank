from .models import User
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwner
# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsOwner,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
