from rest_framework import permissions

class IsOwnerOrModerator(permissions.BasePermission):
    """
    Разрешение, которое позволяет редактировать или удалять объект, если
    пользователь является владельцем объекта или имеет права модератора.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.groups.filter(name="Moderators").exists()
