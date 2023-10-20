from rest_framework.permissions import BasePermission
from home.models import CustomUser


class IsVerified(BasePermission):
    def has_permission(self, request, view):
            user = request.user
            if user.is_anonymous:
                data = request.data
                try:
                    user = CustomUser.objects.get(email=data['email'])
                    return user.is_verified
                except:
                    return False
            else:
                 return user.is_verified

