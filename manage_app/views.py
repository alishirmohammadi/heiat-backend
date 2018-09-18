from rest_framework import generics, views, decorators, response, permissions, viewsets
from .models import *
from .serializers import *


class ManagementList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ManagementListSerializer

    def get_queryset(self):
        return self.request.user.profile.managements.all()
