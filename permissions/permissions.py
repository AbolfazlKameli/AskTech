from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    message = 'You already authenticated!'

    def has_permission(self, request, view):
        return bool(request.user and not request.user.is_authenticated)
