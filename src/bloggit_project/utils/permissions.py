#general permissions for the app

from rest_framework import permissions

from users_app.models import Sub

class AuthenticatedReadAndOwnerOnly(permissions.BasePermission):
    '''allow only safe methods or the owner of the object'''

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        elif request.method in permissions.SAFE_METHODS:
            return True
    
    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return obj.owner.user == request.user
        
        elif request.method in permissions.SAFE_METHODS:
            return True


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "GET"
    def has_object_permission(self, request, view, obj):
        return request.method == "GET"