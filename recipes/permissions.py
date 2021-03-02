from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from rest_framework import permissions

User = get_user_model()


class IsOwnerResourceOrModerator(permissions.BasePermission):
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author == request.user or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()
