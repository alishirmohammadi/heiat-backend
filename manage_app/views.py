from rest_framework import generics, views, decorators, response, permissions, viewsets
from .models import *
from .serializers import *


class ManagementViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.profile.managements.all()

    def get_serializer_class(self):
        return ManagementListSerializer
