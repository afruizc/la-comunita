from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Community, Group, Chat, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Represents the serialization of the user."""
    communities = (serializers
                   .HyperlinkedRelatedField(many=True,
                                            view_name='community-detail',
                                            queryset=Community.objects.all()))
    c_groups = (serializers
                .HyperlinkedRelatedField(many=True,
                                         view_name='group-detail',
                                         queryset=Group.objects.all()))
    chats = (serializers
             .HyperlinkedRelatedField(many=True,
                                      view_name='chat-detail',
                                      queryset=Chat.objects.all()))
    seen_messages = (serializers
                     .HyperlinkedRelatedField(many=True,
                                              view_name='message-detail',
                                              queryset=Message.objects.all()))
    sent_messages = (serializers
                     .HyperlinkedRelatedField(many=True,
                                              view_name='message-detail',
                                              queryset=Message.objects.all()))

    class Meta:
        model = User
        fields = ('username', 'last_login', 'communities',
                  'c_groups', 'chats', 'seen_messages', 'sent_messages')


class JoinableSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name='user-detail')


class CommunitySerializer(JoinableSerializer):
    """Serializer for a community class."""

    class Meta:
        model = Community
        fields = ('name', 'created_on', 'users')


class GroupSerializer(JoinableSerializer):
    """Serializer for a group."""
    community = (serializers
                 .HyperlinkedRelatedField(read_only=True,
                                          view_name='community-detail'))

    class Meta:
        model = Group
        fields = ('name', 'created_on', 'users', 'community')


class ChatSerializer(JoinableSerializer):
    """Serializer for a chat."""
    messages = serializers.HyperlinkedRelatedField(many=True,
                                                   read_only=True,
                                                   view_name='message-detail')
    group = serializers.HyperlinkedRelatedField(read_only=True,
                                                view_name='group-detail')

    class Meta:
        model = Chat
        fields = ('name', 'created_on', 'users', 'messages', 'group')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a message class."""
    chat = (serializers
            .HyperlinkedRelatedField(read_only=True,
                                     view_name='message-detail'))
    sender = serializers.HyperlinkedRelatedField(read_only=True,
                                                 view_name='user-detail')
    seen_by = (serializers
               .HyperlinkedRelatedField(read_only=True,
                                        many=True,
                                        view_name='user-detail'))

    class Meta:
        model = Message
        fields = ('content', 'date_sent', 'sender', 'seen_by', 'chat')
