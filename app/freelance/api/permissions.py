from rest_framework.permissions import BasePermission


class FrelancerPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj.user
        return True


class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return False
        return True
    
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user == obj.user
        return True