from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, SAFE_METHODS

class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_admin


class IsAuthorAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.is_admin
            )
        return False