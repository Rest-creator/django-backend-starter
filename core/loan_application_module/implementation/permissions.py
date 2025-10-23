from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAgent(BasePermission):
    """
    Mark agents via a boolean flag on user profile or group.
    Replace with your own logic (e.g., user.groups.filter(name='Agents').exists())
    """

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "is_agent", False)
        )


class IsAdminReviewer(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_staff
                or getattr(request.user, "is_admin_reviewer", False)
            )
        )


class IsOwnerOrAdmin(BasePermission):
    """
    For object-level access (not used below, but handy if exposing client details).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (getattr(request.user, "is_staff", False)) or (
            obj.created_by_id == request.user.id
        )

class IsAgentOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            getattr(request.user, "is_agent", False) or
            getattr(request.user, "is_superuser", False)
            )
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return (
                getattr(request.user, "is_agent", False) or 
                getattr(request.user, "is_superuser", False)
                )
        return getattr(request.user, "is_superuser", False)