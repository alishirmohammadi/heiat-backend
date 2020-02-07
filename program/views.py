from rest_framework import generics, viewsets, response, decorators

from .pemissions import *
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
def register(request, program_id):
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


class NewMessage(generics.CreateAPIView):
    queryset = Message.objects.filter(to_user=False)
    serializer_class = NewMessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def sub_program_detail(request, program_id, sub_program_id):
    username = request.data.get("username")
    if not username:
        return response.Response({"message": "نام کاربری فرستاده نشده است.", "ok": False})
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return response.Response({"message": "کاربر وارد شده وجود ندارد.", "ok": False})
    program = Program.objects.filter(id=program_id).first()
    if not program:
        return response.Response({"message": "برنامهٔ وارد شده وجود ندارد.", "ok": False})
    registration = Registration.objects.filter(program=program, profile=profile).first()
    if not registration:
        return response.Response({"message": "کاربر در برنامهٔ مورد نظر ثبت‌نام نکرده است.", "ok": False})
    if registration.numberOfPayments == 0:
        return response.Response({"ok": False, "message": "شما هزینهٔ شرکت در برنامه را پرداخت نکرده اید."})
    sub_program = (lambda a: {
        "59": "سرزمین موج‌های آبی",
        "60": "پینت بال",
        "61": "فوتسال",
        "76": "بولینگ",
        "77": "دیدار با خانواده شهدا",
        "78": "بازدید از آسایشگاه معلولین فیاض‌بخش",
        "79": "بازدید از آسایشگاه جانبازان امام خمینی (ره)",
    }[a])(sub_program_id)
    question = Question.objects.get(id=sub_program_id)
    answer = Answer.objects.filter(question=question, profile=profile).first()
    if not answer:
        answer = False
    else:
        answer = answer.yes
    if not answer:
        return response.Response({
            "ok": False,
            "message": "خطا. شما در برنامهٔ %s شرکت نکرده اید." % sub_program
        })
    return response.Response({
        "ok": True,
        "message": "شما می‌توانید در برنامهٔ %s شرکت کنید." % sub_program
    })
