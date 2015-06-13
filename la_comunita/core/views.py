from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Community
from .serializers import CommunitySerializer, UserSerializer


class UserViewClass(viewsets.UserSerializer):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
