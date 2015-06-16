"""
Module that defines the signal handlers for the application.
"""

from django.conf import settings
from django.db.models.signals import (post_save, m2m_changed)
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from core.models import Group


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(m2m_changed, sender=Group.users.through)
def check_group_active(sender, instance=None, action='',
                       reverse=False, **kwargs):
    if action.startswith('post') and not reverse:
        if instance.users.count() >= 3:
            instance.active = True
        else:
            instance.active = False

        if instance.users.count() == 0:
            instance.delete()
