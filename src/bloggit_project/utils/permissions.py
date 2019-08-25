#general permissions for the app

from rest_framework import permissions

class ReadOrOwnerOnly(permissions.BasePermission):
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


class AuthenticatedAndOwnerOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        authenticated = request.user.is_authenticated
        methods_allowed = ["POST", "PUT", "DELETE"]
        
        if authenticated == True and request.method in methods_allowed:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner.user