from rest_framework import permissions
from apps.users.models import User
class IsCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user:User = request.user
        return user.is_authenticated and user.role == 'company' or user.is_superuser

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.item.company.owner == request.user


class ItemPaymentPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        user:User = request.user
        return user.is_authenticated and user.role == 'company'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.item.company.owner == request.user