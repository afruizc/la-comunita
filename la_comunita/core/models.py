from django.contrib.auth.models import User
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


class PrivateChat(Joinable):
    """Represents a private chat that is joined by exactly two users."""

    class Meta:
        default_related_name = 'private_chats'


class GroupChat(Joinable):
    """Represents a chat that happens in a group. This type of chat
    can have many users and the messages are delivered to all
    of them.
    """
    group = models.ForeignKey(Group, related_name='chats')

    class Meta:
        default_related_name = 'group_chats'


class Message(models.Model):
    """Represents a message sent on the chat."""
    date_sent = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    sender = models.ForeignKey(User, related_name='%(class)s_sent')
    seen_by = models.ManyToManyField(User, related_name='%(class)s_seen')

    class Meta:
        abstract = True


class GroupMessage(Message):
    chat = models.ForeignKey('GroupChat', related_name='messages')


class PrivateMessage(Message):
    chat = models.ForeignKey('PrivateChat', related_name='messages')
