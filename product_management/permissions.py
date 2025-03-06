from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission that allows access only to users with the role 'admin'.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'