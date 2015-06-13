from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Community, Group, PrivateChat, GroupChat, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Represents the serialization of the user."""
    # TODO: Add communities, groups, private_chats, group_chats
    # seen_messages, sent_messages,
    class Meta:
        model = User


class JoinableSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True)


class CommunitySerializer(JoinableSerializer):
    """Serializer for a community class."""

    class Meta:
        model = Community
        fields = ('name', 'created_on', 'users')


class GroupSerializer(JoinableSerializer):
    """Serializer for a group."""
    community = serializers.HyperlinkedRelatedField(read_only=True)

    class Meta:
        model = Group
        fields = ('name', 'created_on', 'users', 'community')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a message class."""
    sender = serializers.HyperlinkedRelatedField(read_only=True)
    seen_by = serializers.HyperlinkedRelatedField(many=True)
    chat = serializers.HyperlinkedRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = ('content', 'date_sent', 'sender', 'seen_by', 'chat')


class ChatSerializer(JoinableSerializer):
    """Serializer for a generic chat."""
    messages = serializers.HyperlinkedRelatedField(many=True,
                                                   read_only=True)

    class Meta:
        fields = ('name', 'created_on', 'users', 'messages')


class PrivateChatSerializer(JoinableSerializer):
    """Serializer for a private chat."""

    class Meta:
        model = PrivateChat


class GroupChatSerializer(JoinableSerializer):
    """Serializer for a group chat."""
    group = serializers.HyperlinkedRelatedField(read_only=True)

    class Meta:
        model = GroupChat
        fields = ('name', 'created_on', 'users', 'messages', 'group')
