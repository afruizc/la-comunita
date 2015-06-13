from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import Community, Group, Chat, Message
from .serializers import (CommunitySerializer, UserSerializer, GroupSerializer,
                          ChatSerializer, MessageSerializer)


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


class ChatViewSet(viewsets.ModelViewSet):
    """Exposes the API for the private chats."""
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class MessageViewSet(viewsets.ModelViewSet):
    """Exposes API for messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
