from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from core.models import (User, Group, Community, Chat,
                         Message, ChatInvitation, GroupInvitation)


def populate_database():
    User.objects.create_user('test1', 'test1@test.t', 'test1')

    u = User.objects.create_user('user1', 'user1@test.t', 'user1')
    c = Community.objects.create(name='community1')
    g = Group.objects.create(name='group1', community=c)
    c = Chat.objects.create(name='group_chat1', group=g)
    Message.objects.create(content='test', sender=u,
                           chat=c)


class TestUserAssociationWithJoinableFromUrls(APITestCase):
    """User being associated with the entities she
    creates."""

    def setUp(self):
        populate_database()
        self.user = User.objects.get(username='user1')
        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_add_group_tied_to_user(self):
        """Creates a group that has as only member the user
        that created it.
        """
        url = reverse('group-list')
        community = Community.objects.first()
        community_link = '/communities/%d/' % community.id
        self.client.post(url, data={'name': 'group_test',
                                    'community': community_link})
        group = Group.objects.get(name='group_test')
        self.assertTrue(group.users.filter(id=self.user.id).exists())

    def test_add_chat_tied_to_user(self):
        """Creates a group chat that has as only member the
        user who create it.
        """
        url = reverse('chat-list')
        group = Group.objects.first()
        group_url = '/groups/%d/' % group.id
        self.client.post(url,
                         data={'name': 'group_chat_test',
                               'group': group_url})
        chat = self.user.chats.filter(name='group_chat_test')
        self.assertTrue(chat.exists())

    def test_add_message_with_sender(self):
        """Creates a message that has as sender the
        user who create it.
        """
        url = reverse('message-list')
        chat = Chat.objects.first()
        chat_url = '/chats/%d/' % chat.id
        self.client.post(url,
                         data={'chat': chat_url,
                               'content': 'test'})
        message = Message.objects.filter(sender=self.user)
        self.assertTrue(message)

    def test_add_group_invitation_tied_to_user(self):
        """Creates a group invitation that has as
        inviter the user who created it.
        """
        url = reverse('groupinvitation-list')
        group = Group.objects.first()
        invitee = User.objects.get(username='test1')
        data = {
            'group': '/groups/%d/' % group.id,
            'invitee': '/users/%d/' % invitee.id
        }
        response = self.client.post(url, data=data)
        group_invitation = GroupInvitation.objects.filter(inviter=self.user)
        self.assertEquals(response.status_code, 201)
        self.assertTrue(group_invitation.exists())

    def test_add_chat_invitation_tied_to_user(self):
        """Creates a chat invitation that has as
        inviter the user who created it.
        """
        url = reverse('chatinvitation-list')
        chat = Chat.objects.first()
        invitee = User.objects.get(username='test1')
        data = {
            'chat': '/chats/%d/' % chat.id,
            'invitee': '/users/%d/' % invitee.id
        }
        response = self.client.post(url, data=data)
        chat_invitation = ChatInvitation.objects.filter(inviter=self.user)
        self.assertEquals(response.status_code, 201)
        self.assertTrue(chat_invitation.exists())
