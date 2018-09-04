from rest_framework import generics, permissions
from .models import *
from .serializers import *


class ProgramList(generics.ListAPIView):
    serializer_class = ProgramListSerializer

    def get_queryset(self):
        queryset = Program.objects.filter(state=Program.STATE_ACTIVE)
        if self.request.user.is_authenticated:
            queryset = queryset | Program.objects.filter(state=Program.STATE_ARCHIVE).filter(
                id__in=self.request.user.profile.registrations.all().values_list('program_id', flat=True))
        return queryset
