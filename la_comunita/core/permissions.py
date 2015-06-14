from rest_framework import permissions


class BelongsTo(permissions.BasePermission):
    """Custom permission to allow users to see instance of a class
    only if they blong to such instance.

    This is intended to be used with classes that inherit from
    ..:class:`core.models.Joinable` and therefore have a set of
    users. The instance is only visible if they user belongs to it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.users.filter(pk=request.user.pk).exists()
