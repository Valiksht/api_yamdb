from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = User.objects.filter(username=request.data.get('username')).first()
        is_admin_user = False
        # print(request.user.is_superuser)
        # print(request.user)
        # print(request.data.get('username'))
        # print(user)
        if user != None:
            # print(user)
            if user.role == 'admin':
                is_admin_user = True
                return is_admin_user
            
        if request.user.is_authenticated:
            if request.user.role == 'admin':
                is_admin_user = True
                return is_admin_user

        # print(is_admin_user)
        
        return (is_admin_user
                or request.user.is_superuser
                # or user.is_superuser
                # or request.user.role == 'admin'
        )
