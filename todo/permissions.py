from rest_framework.permissions import BasePermission


class UnauthenticatedWritePermission(BasePermission):
    """
    Allow write operations for unauthenticated users.
    """

    def has_permission(self, request, view):
        return not request.user or not request.user.is_authenticated
