from django.contrib.auth.models import User
from rest_framework import viewsets

from .models import (Community, Group, Chat, Message, GroupInvitation,
                     ChatInvitation)
from .serializers import (CommunitySerializer, UserSerializer, GroupSerializer,
                          GroupInvitationSerializer, ChatInvitationSerializer,
                          ChatSerializer, MessageSerializer)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
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

    def perform_create(self, serializer):
        """Adds the user that created the group
        as a member.
        """
        g_obj = serializer.save()
        g_obj.users.add(self.request.user)


class ChatViewSet(viewsets.ModelViewSet):
    """Exposes the API for the private chats."""
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def perform_create(self, serializer):
        c_obj = serializer.save()
        c_obj.users.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """Exposes API for messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        """Sets the sender to be the current user."""
        serializer.save(sender=self.request.user)


class GroupInvitationViewSet(viewsets.ModelViewSet):
    """Exposes API for Group Invitations"""
    queryset = GroupInvitation.objects.all()
    serializer_class = GroupInvitationSerializer

    def perform_create(self, serializer):
        """Sets the inviter to be the current user."""
        serializer.save(inviter=self.request.user)


class ChatInvitationSerializer(viewsets.ModelViewSet):
    """Exposes API for chat invitations"""
    queryset = ChatInvitation.objects.all()
    serializer_class = ChatInvitationSerializer

    def perform_create(self, serializer):
        """Sets the inviter to be the current user."""
        serializer.save(inviter=self.request.user)
