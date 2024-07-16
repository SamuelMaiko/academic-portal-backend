from rest_framework.permissions import BasePermission

class IsWorkWriter(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return request.user==obj.writer
