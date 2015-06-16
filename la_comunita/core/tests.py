from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from core.models import User, Group, Community


def populate_database():
    User.objects.create_user('test1', 'test1@test.t', 'test1')
    User.objects.create_user('test2', 'test2@test.t', 'test2')
    User.objects.create_user('test3', 'test3@test.t', 'test3')

    Community.objects.create(name='community1')


class TestUserAssociationFromUrls(APITestCase):
    """User being associated with the entities she
    creates."""

    def setUp(self):
        populate_database()

    def test_add_group_with_user(self):
        """Creates a group that has as only member the user
        that created it.
        """
        url = reverse('group-list')
        token = Token.objects.get(user__username='test1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        community = Community.objects.first()
        community_link = '/communities/%d/' % community.id
        self.client.post(url, data={'name': 'group1',
                                    'community': community_link})
        group = Group.objects.get(name='group1')
        user = User.objects.get(username='test1')
        self.assertIn(user, group.users.all())
