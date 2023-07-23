from rest_framework import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            # Allow all authenticated users to have permission for safe methods (e.g., GET, HEAD, OPTIONS)
            if request.method in SAFE_METHODS:
                return True

            # Check if the authenticated user is an admin
            return request.user.is_staff

        # Deny permissions for all other non-safe methods for anonymous users (e.g., POST, PUT, PATCH, DELETE)
        return request.method in SAFE_METHODS
