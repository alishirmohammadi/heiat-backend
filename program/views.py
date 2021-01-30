from rest_framework import generics, viewsets, response, decorators

from .pemissions import *
from .serializers import *

import base64
from django.core.files.base import ContentFile
import uuid

class ProgramViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return ProgramListSerializer
        return ProgramDetailSerializer

    def get_queryset(self):
        queryset = Program.objects.filter(state=Program.STATE_ACTIVE)
        if self.request.user.is_authenticated:
            queryset = queryset | Program.objects.filter(state=Program.STATE_ARCHIVE).filter(
                id__in=self.request.user.profile.registrations.exclude(status=RegisterState.STATUS_REMOVED).values_list(
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
    if not registration.status in [RegisterState.STATUS_CERTAIN, RegisterState.STATUS_RESERVED,
                                   RegisterState.STATUS_DEFAULT]:
        return response.Response('درخواست نامعتبر', status=400)
    registration.status = RegisterState.STATUS_GIVEN_UP
    registration.save()
    if registration.coupling:
        cr = registration.get_couple_registration()
        if cr:
            cr.status = RegisterState.STATUS_GIVEN_UP
            cr.save()
    return response.Response('ok')


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def register(request, program_id):
    program = Program.objects.filter(id=program_id).first()
    if not program or program.state != Program.STATE_ACTIVE or not program.is_open:
        return response.Response('درخواست نامعتبر', status=400)
    reg = Registration.objects.filter(program=program).filter(profile__user=request.user).exclude(
        status=RegisterState.STATUS_REMOVED).first()
    if reg:
        return response.Response('قبلا ثبت‌نام کرده‌اید', status=400)
    reg = Registration.objects.create(
        program=program,
        profile=request.user.profile,
        status=program.default_status,
    )
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
            text = answer.get('answer_text', None)
            print(text)
            print(answer)
            ans, _ = Answer.objects.update_or_create(question=question, registration=reg, answer_text=text, defaults={'yes': yes})
            if couple_reg:
                Answer.objects.update_or_create(question=question, registration=couple_reg, answer_text=text, defaults={'yes': yes})
            ans_file = answer.get('answer_file', None)
            if ans_file:
                format, imgstr = ans_file.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr))
                file_name = uuid.uuid1().hex + '.' + ext
                ans.answer_file.save(file_name, data, save=True)

    return response.Response(RegistrationInProgramDetailSerializer(reg).data)


class NewMessage(generics.CreateAPIView):
    queryset = Message.objects.filter(to_user=False)
    serializer_class = NewMessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


cultural_to_question = {}
cultural_to_persian = {}


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def cultural_program(request, sub_program):
    if sub_program not in cultural_to_question.keys():
        return response.Response({"ok": False, "message": "invalid subprogram name."})
    username = request.data.get('username')
    if not username:
        return response.Response({"ok": False, "message": "username not sent"})
    profile = Profile.objects.get(user__username=username)
    if not profile:
        return response.Response({"ok": False, "message": "user with this username not found"})
    user_json = {"name": profile.__str__()}
    program = Program.objects.filter(title="برنامه‌های فرهنگی پابوس عشق ۹۸").first()
    if not program:
        return response.Response({"ok": False, "user": user_json, "message": "program not found"})
    reg = Registration.objects.filter(profile=profile, program=program).first()
    if not reg:
        return response.Response(
            {"ok": False, "user": user_json, "message": "شما در هیچ یک از برنامه‌های فرهنگی ثبت نام نکرده اید."})
    question = cultural_to_question[sub_program]
    answer = Answer.objects.filter(question=question, registration=reg).first()
    if not answer:
        return response.Response({"ok": False, "user": user_json,
                                  "message": "شما در برنامهٔ %s شرکت نکرده اید." % cultural_to_persian[sub_program]})
    if not answer.yes:
        return response.Response({"ok": False, "user": user_json,
                                  "message": "شما در برنامهٔ %s شرکت نکرده اید." % cultural_to_persian[sub_program]})
    return response.Response({"ok": True, "user": user_json, "message": "شما در برنامه شرکت کرده اید."})


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAdminUser,))
def cultural_history(request, sub_program):
    return response.Response(
        {"ok": False, "meal": {"title": "عنوان", "food": "نام غذا", "total": 1000, "receipt_count": 10},
         "message": "این بخش در حال پیاده سازی می‌باشد..."})


sub_program_to_question = {}
sub_program_to_persian = {}


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def entertainment_program(request, sub_program):
    if sub_program not in sub_program_to_question.keys():
        return response.Response({"ok": False, "message": "invalid subprogram name."})
    username = request.data.get('username')
    if not username:
        return response.Response({"ok": False, "message": "username not sent"})
    profile = Profile.objects.get(user__username=username)
    if not profile:
        return response.Response({"ok": False, "message": "user with this username not found"})
    user_json = {"name": profile.__str__()}
    program = Program.objects.filter(title="برنامه‌های جانبی پابوس عشق ۹۸ خواهران").first()
    if not program:
        return response.Response({"ok": False, "user": user_json, "message": "program not found"})
    reg = Registration.objects.filter(profile=profile, program=program).first()
    if not reg:
        return response.Response(
            {"ok": False, "user": user_json, "message": "شما در هیچ یک از برنامه‌های تفریحی ثبت نام نکرده اید."})
    question = sub_program_to_question[sub_program]
    answer = Answer.objects.filter(question=question, registration=reg).first()
    if not answer:
        return response.Response({"ok": False, "user": user_json,
                                  "message": "شما در برنامهٔ %s شرکت نکرده اید." % sub_program_to_persian[sub_program]})
    if not answer.yes:
        return response.Response({"ok": False, "user": user_json,
                                  "message": "شما در برنامهٔ %s شرکت نکرده اید." % sub_program_to_persian[sub_program]})
    if reg.numberOfPayments == 0:
        return response.Response(
            {"ok": False, "user": user_json, "message": "شما هزینهٔ شرکت در برنامه را پرداخت نکرده اید."})
    return response.Response({"ok": True, "user": user_json, "message": "شما در برنامه شرکت کرده اید."})


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAdminUser,))
def entertainment_history(request, sub_program):
    return response.Response(
        {"ok": False, "meal": {"title": "عنوان", "food": "نام غذا", "total": 1000, "receipt_count": 10},
         "message": "این بخش در حال پیاده سازی می‌باشد..."})
