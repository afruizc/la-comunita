"""
Configuration for the app. Mostly necessary to load
the signals that will be handled by the app.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'La Comunita Core'

    def ready(self):
        from core.signals import handlers  # NOQA: This is ok
