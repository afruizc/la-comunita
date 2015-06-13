from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Joinable(models.Model):
    """Class that holds information about the things
    that a User can Join. Specifically, a user can join
    a Community, a Group and a Chat.

    .. note:: This is an abstract class that holds information
             about these entities.
    """
    name = models.CharField(max_length=100)
    created_on = models.DateTimeField('creation date', auto_now_add=True)
    users = models.ManyToManyField(User)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Community(Joinable):
    """Represents a community that is joined
    by several users. Right now, because we are dealing
    with the first protype, this class has nothing on it.
    """
    pass

    class Meta:
        default_related_name = 'communities'


class Group(Joinable):
    """Represents a group that is created inside of a community.
    This group is created by the users and needs to have at least
    5 users in it in order to be active.
    """
    activity = models.FloatField(default=0.0)
    community = models.ForeignKey(Community, related_name='groups')
    is_active = models.BooleanField(default=False)

    class Meta:
        default_related_name = 'c_groups'

    def __str__(self):
        return (self.is_active and '[active]' or '[inactive]' +
                super(Group, self).__str__())


class Message(models.Model):
    """Represents a message sent on the chat."""
    date_sent = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    seen_by = models.ManyToManyField(User, related_name='seen_messages')
    sender = models.ForeignKey(User, related_name='sent_messages')
    chat_ct = models.ForeignKey(ContentType)
    chat_oi = models.PositiveIntegerField()
    chat = GenericForeignKey('chat_ct', 'chat_oi')


class Chat(Joinable):
    """Represents a generic chat between two or more entities."""

    class Meta:
        abstract = True


class PrivateChat(Chat):
    """Represents a private chat that is joined by exactly two users."""
    messages = GenericRelation(Message,
                               related_query_name='private_messages',
                               content_type_field='chat_ct',
                               object_id_field='chat_oi')

    class Meta:
        default_related_name = 'private_chats'


class GroupChat(Chat):
    """Represents a chat that happens in a group. This type of chat
    can have many users and the messages are delivered to all
    of them.
    """
    messages = GenericRelation(Message,
                               related_query_name='group_messages',
                               content_type_field='chat_ct',
                               object_id_field='chat_oi')
    group = models.ForeignKey(Group, related_name='chats')

    class Meta:
        default_related_name = 'group_chats'
