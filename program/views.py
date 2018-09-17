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


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def register(request,program_id):
    program = Program.objects.filter(id=program_id).first()
    if not program or program.state != Program.STATE_ACTIVE or not program.is_open:
        return response.Response('درخواست نامعتبر', status=400)
    reg = Registration.objects.filter(program=program).filter(profile__user=request.user).exclude(
        status=Registration.STATUS_REMOVED).first()
    if reg:
        return response.Response('قبلا ثبت‌نام کرده‌اید', status=400)
    reg = Registration.objects.create(program=program, profile=request.user.profile)
    couple_reg = None
    coupling = request.data.get('coupling', False)
    if program.has_coupling and request.user.profile.couple and coupling:
        reg.coupling = True
        reg.save()
        couple_reg, created = Registration.objects.update_or_create(program=program,
                                                                    profile=request.user.profile.couple,
                                                                    defaults={'coupling': True})
    answers = request.data.get('answers', [])
    for answer in answers:
        question_id = answer.get('question_id', None)
        question = Question.objects.filter(id=question_id).first()
        if question and question.user_sees and question.program == program:
            yes = answer.get('yes', False)
            Answer.objects.update_or_create(question=question, registration=reg, defaults={'yes': yes})
            if couple_reg:
                Answer.objects.update_or_create(question=question, registration=couple_reg, defaults={'yes': yes})
    return response.Response(RegistrationInProgramDetailSerializer(reg).data)
