from rest_framework import generics, permissions, viewsets, response, decorators
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


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def give_up(request):
    registration_id = request.data.get('registration_id')
    if not registration_id:
        return response.Response('درخواست نامعتبر', status=400)
    registration = Registration.objects.filter(id=registration_id).first()
    if not registration or registration.profile.user.username != request.user.username:
        return response.Response('درخواست نامعتبر', status=400)
    if not registration.status in [Registration.STATUS_CERTAIN, Registration.STATUS_RESERVED,
                                   Registration.STATUS_DEFAULT]:
        return response.Response('درخواست نامعتبر', status=400)
    registration.status = Registration.STATUS_GIVEN_UP
    registration.save()
    if registration.coupling:
        cr = registration.get_couple_registration()
        if cr:
            cr.status = Registration.STATUS_GIVEN_UP
            cr.save()
    return response.Response('ok')
