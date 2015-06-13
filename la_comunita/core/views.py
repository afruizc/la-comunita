from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Community, Group
from .serializers import CommunitySerializer, UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """View that exposes the general methods for
    a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommunityViewSet(viewsets.ModelViewSet):
    """View that exposes the general methods for
    a community."""
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


class GroupViewSet(viewsets.ModelViewSet):
    """View that exposes the API for the groups."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
