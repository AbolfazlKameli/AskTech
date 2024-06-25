from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    message = 'You already authenticated'

    def has_permission(self, request, view):
        return request.user and not request.user.is_authenticated


class IsActiveUser(BasePermission):
    message = 'Your account is not activated'

    def has_permission(self, request, view):
        return request.user and request.user.is_active and request.user.is_authenticated
