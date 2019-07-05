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
            print(request.user)
            return obj.owner.user.username == request.user.username
        
        elif request.method in permissions.SAFE_METHODS:
            return True