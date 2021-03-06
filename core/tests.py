from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status

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
        print(self.user)
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


class TestChatAcceptRejectInvitation(APITestCase):
    """Mechanics for accepting and rejecting invitations. Due
    to the fact that GroupInvitation and ChatInvitation share
    a lot of behavior, only the latter class is tested. The former,
    by extension, is assumed to be correct.
    """

    def setUp(self):
        User.objects.create_user('test1', 't@t.t', 'test1')
        c = Chat.objects.create(name='chat1')
        self.user = User.objects.create_user('user1', 'u@u.u', 'user1')
        token = Token.objects.get(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        self.invitee = User.objects.get(username='test1')
        self.invitation = ChatInvitation.objects.create(
            inviter=self.user,
            invitee=self.invitee,
            chat=c)

    def perform_action(self, action, token):
        """Performs the given action to an invitation.

        :param action: action taken with respect to the invitation.
                       (accept/reject and invitation).
        :type action: str.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post('/chatinvitations/%d/%s/' %
                                    (self.invitation.id, action))
        return (response, self.invitee.received_chatinvitations.get(
            id=self.invitation.id))

    def perform_action_by_invitee(self, action):
        """Performs the given action by the invitee. This
        uses the `perform_action` method and sets the auth
        token for the invitee user.
        """
        token = Token.objects.get(user=self.invitee).key
        response, invitation = self.perform_action(action, token)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        return invitation

    def test_accept_invitation(self):
        """Invitee accepts the invitation"""
        invitation = self.perform_action_by_invitee('accept')
        self.assertTrue(invitation.accepted)
        self.assertIn(self.invitation.chat, self.invitee.chats.all())

    def test_reject_invitation(self):
        """User does not accept the invitation"""
        invitation = self.perform_action_by_invitee('reject')
        self.assertFalse(invitation.accepted)
        self.assertNotIn(self.invitation.chat, self.invitee.chats.all())

    def test_wrong_user_accepts(self):
        """Wrong user accepts the invitation"""
        token = Token.objects.get(user__username='user1').key
        response, invitation = self.perform_action('accept', token)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)


class TestSentReceivedChatInvitations(APITestCase):
    """Tests views for gettting the invitations that a user has
    sent and received. Same as before, we only test `ChatInvitation`"""

    def setUp(self):
        """Create 3 users, u1, u2 and u3. Each one of these is going
        to send 2 invitations to the other two, so in total, every
        user will have 2 sent invitations and 2 received invitations."""
        self.u1 = User.objects.create_user('u1', 'u1@u1.u1', 'u1')
        self.u2 = User.objects.create_user('u2', 'u2@u2.u2', 'u1')
        c = Chat.objects.create(name='c1')
        ChatInvitation.objects.create(
            inviter=self.u1,
            invitee=self.u2,
            chat=c
        )

    def check_invitations(self, user, type_):
        """Checks that the specific type of invitations belong to
        the user."""
        t = Token.objects.get(user=user).key
        should_be = ['http://testserver/chatinvitations/1/']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + t)
        response = self.client.get('/chatinvitations/%s/' % type_)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        received = [x['url'] for x in response.data['results']]
        self.assertListEqual(should_be, received)

    def test_sent_invitations(self):
        """User sees received invitations."""
        self.check_invitations(self.u1, 'sent')

    def test_received_invitations(self):
        """User sees sent invitations."""
        self.check_invitations(self.u2, 'received')
