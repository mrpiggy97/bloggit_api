#general permissions for the app

from rest_framework import permissions

class ReadOrOwnerONly(permissions.BasePermission):
    '''allow only safe methods or the owner of the object'''

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
    
    def has_object_permission(self, request, view, obj):
        return obj.sub.user == request.user