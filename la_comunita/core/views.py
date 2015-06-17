from django.contrib.auth.models import User
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from .models import (Community, Group, Chat, Message, GroupInvitation,
                     ChatInvitation)
from .serializers import (CommunitySerializer, UserSerializer, GroupSerializer,
                          GroupInvitationSerializer, ChatInvitationSerializer,
                          ChatSerializer, MessageSerializer)
from .permissions import BelongsTo


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """View that exposes the general methods for
    a user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CommunityViewSet(viewsets.ModelViewSet):
    """View that exposes the general methods for
    a community."""
    serializer_class = CommunitySerializer
    permissions_classes = (BelongsTo,)

    def get_queryset(self):
        """Returns the communities to which the
        current user belongs to.
        """
        user = self.request.user
        return Community.objects.filter(users=user)


class GroupViewSet(viewsets.ModelViewSet):
    """View that exposes the API for the groups."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permissions_classes = (BelongsTo,)

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
    permissions_classes = (BelongsTo,)

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


class InvitationViewSet(viewsets.ModelViewSet):
    """Parent class to abstract operations performed
    over an Invitation."""

    def perform_create(self, serializer):
        """Sets the inviter to be the current user."""
        serializer.save(inviter=self.request.user)

    @detail_route(methods=['post'])
    def reject(self, request, pk=None):
        invite_obj = self.get_object()
        invite_obj.accepted = False
        invite_obj.save()

        return Response(status=status.HTTP_200_OK)


class GroupInvitationViewSet(InvitationViewSet):
    """Exposes API for Group Invitations"""
    queryset = GroupInvitation.objects.all()
    serializer_class = GroupInvitationSerializer

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        invite_obj = self.get_object()
        invite_obj.accepted = True
        invite_obj.group.users.add(request.user)
        invite_obj.save()

        return Response(status=status.HTTP_200_OK)


class ChatInvitationViewSet(InvitationViewSet):
    """Exposes API for chat invitations"""
    queryset = ChatInvitation.objects.all()
    serializer_class = ChatInvitationSerializer

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        invite_obj = self.get_object()
        invite_obj.accepted = True
        invite_obj.chat.users.add(request.user)
        invite_obj.save()

        return Response(status=status.HTTP_200_OK)
