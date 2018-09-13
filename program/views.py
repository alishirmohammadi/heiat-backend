from rest_framework import generics, permissions, viewsets
from .models import *
from .serializers import *


class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return ProgramListSerializer
        return ProgramDetailSerializer

    def get_queryset(self):
        queryset = Program.objects.filter(state=Program.STATE_ACTIVE)
        if self.request.user.is_authenticated:
            queryset = queryset | Program.objects.filter(state=Program.STATE_ARCHIVE).filter(
                id__in=self.request.user.profile.registrations.exclude(status=Registration.STATUS_REMOVED).values_list(
                    'program_id', flat=True))
        return queryset
