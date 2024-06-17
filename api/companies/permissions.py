from rest_framework import permissions


class IsCompanyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role == 'company'