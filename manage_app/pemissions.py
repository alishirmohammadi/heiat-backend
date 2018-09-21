from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.managements.all() & request.user.profile.managements.all()


class IsManagerOfProgram(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.program.managements.all() & request.user.profile.managements.all()
