from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Community, Group, Chat, Message


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Represents the serialization of the user."""
    communities = (serializers
                   .HyperlinkedRelatedField(many=True,
                                            view_name='community-detail',
                                            read_only=True))
    c_groups = (serializers
                .HyperlinkedRelatedField(many=True,
                                         view_name='group-detail',
                                         read_only=True))
    chats = (serializers
             .HyperlinkedRelatedField(many=True,
                                      view_name='chat-detail',
                                      read_only=True))
    seen_messages = (serializers
                     .HyperlinkedRelatedField(many=True,
                                              view_name='message-detail',
                                              read_only=True))
    sent_messages = (serializers
                     .HyperlinkedRelatedField(many=True,
                                              view_name='message-detail',
                                              read_only=True))

    class Meta:
        model = User
        fields = ('url', 'username', 'last_login', 'communities',
                  'c_groups', 'chats', 'seen_messages', 'sent_messages')


class JoinableSerializer(serializers.HyperlinkedModelSerializer):
    users = serializers.HyperlinkedRelatedField(many=True,
                                                read_only=True,
                                                view_name='user-detail')


class CommunitySerializer(JoinableSerializer):
    """Serializer for a community class."""

    class Meta:
        model = Community
        fields = ('url', 'name', 'created_on', 'users')


class GroupSerializer(JoinableSerializer):
    """Serializer for a group."""
    community = (serializers
                 .HyperlinkedRelatedField(
                     view_name='community-detail',
                     queryset=Community.objects.all()))

    class Meta:
        model = Group
        fields = ('url', 'name', 'created_on', 'users', 'community')


class ChatSerializer(JoinableSerializer):
    """Serializer for a chat."""
    messages = serializers.HyperlinkedRelatedField(many=True,
                                                   read_only=True,
                                                   view_name='message-detail')
    group = serializers.HyperlinkedRelatedField(queryset=Group.objects.all(),
                                                view_name='group-detail')

    class Meta:
        model = Chat
        fields = ('url', 'name', 'created_on', 'users', 'messages', 'group')


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a message class."""
    chat = (serializers
            .HyperlinkedRelatedField(queryset=Chat.objects.all(),
                                     view_name='chat-detail'))
    sender = serializers.HyperlinkedRelatedField(queryset=User.objects.all(),
                                                 view_name='user-detail')
    seen_by = (serializers
               .HyperlinkedRelatedField(read_only=True,
                                        many=True,
                                        view_name='user-detail'))

    class Meta:
        model = Message
        fields = ('url', 'content', 'date_sent', 'sender', 'seen_by', 'chat')
