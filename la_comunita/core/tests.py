from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from core.models import (User, Group, Community, Chat,
                         Message, ChatInvitation, GroupInvitation)


class TestUserAssociationWithJoinableFromUrls(APITestCase):
    """User being associated with the entities she
    creates."""

    def setUp(self):
        User.objects.create_user('test1', 'test1@test.t', 'test1')

        u = User.objects.create_user('user1', 'user1@test.t', 'user1')
        c = Community.objects.create(name='community1')
        g = Group.objects.create(name='group1', community=c)
        c = Chat.objects.create(name='group_chat1', group=g)
        Message.objects.create(content='test', sender=u,
                               chat=c)
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


class TestFilterEntitiesByLoggedUser(APITestCase):
    """Only the entities associated with the current user
    are returned.
    """

    def setUp(self):
        tu1 = User.objects.create_user('test1', 'test1@test.t', 'test1')
        tu2 = User.objects.create_user('test2', 'test2@test.t', 'test2')
        # tu3 = User.objects.create_user('test3', 'test2@test.t', 'test3')

        u = User.objects.create_user('user1', 'user1@test.t', 'user1')
        c = Community.objects.create(name='community1')
        c.users.add(u, tu1, tu2)
        g = Group.objects.create(name='group1', community=c)
        self.c = c
        c = Chat.objects.create(name='group_chat1', group=g)
        c.users.add(u, tu1, tu2)
        Message.objects.create(content='test', sender=u,
                               chat=c)
        self.user = User.objects.get(username='user1')
        self.token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_get_communities_of_logged_user(self):
        """Returns communities of the logged user"""
        response = self.client.get('/communities/')
        communities_response = [x['url'] for x in response.data['results']]
        communities_user = ['http://testserver/communities/%d/' % x.id
                            for x in self.user.communities.all()]
        self.assertListEqual(communities_response, communities_user)

    def test_groups_of_logged_user(self):
        """Returns groups of the logged user."""
        url_c = reverse('community-list') + '%d/'
        for i in range(3):
            with self.subTest(i=i):
                data = {'name': 'group_test%d' % i,
                        'community': url_c % self.c.id}
                response = self.client.post('/groups/', data=data)
                self.assertEquals(response.status_code, 201)

        response = self.client.get('/groups/')
        groups_response = [x['url'] for x in response.data['results']]
        groups_user = ['http://testserver/groups/%d/' % x.id
                       for x in self.user.c_groups.all()]
        self.assertListEqual(groups_response, groups_user)


class TestChatInvitation(APITestCase):
    """Mechanics for accepting and rejecting invitations."""

    def setUp(self):
        User.objects.create_user('test1', 't@t.t', 'test1')
        c = Chat.objects.create(name='chat1')

        self.user = User.objects.get(username='user1')
        token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.invitee = User.objects.get(username='test1')
        self.invitation = ChatInvitation.objects.create(
            inviter=self.user,
            invitee=self.invitee,
            chat=c)

    def test_user_accept_invitation(self):
        new_token = Token.objects.get(user=self.invitee).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token)
        response = self.client.post('/chatinvitations/%d/accept/' %
                                    self.invitation.id)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(self.invitee
                        .received_chatinvitations.first()
                        .accepted)
        self.assertIn(self.invitation.chat, self.invitee.chats.all())

    def test_reject_invitation(self):
        new_token = Token.objects.get(user=self.invitee).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + new_token)
        response = self.client.post('/chatinvitations/%d/reject/' %
                                    self.invitation.id)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(self.invitee
                         .received_chatinvitations.first()
                         .accepted)
        self.assertNotIn(self.invitation.chat, self.invitee.chats.all())
