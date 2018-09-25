from rest_framework import generics, views, decorators, response, permissions, viewsets, mixins, status
from .models import *
from .serializers import *
from .pemissions import *


class ManagementList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ManagementListSerializer

    def get_queryset(self):
        return self.request.user.profile.managements.all()


class RegistrationManagement(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = (permissions.IsAuthenticated, IsManagerOfProgram)
    serializer_class = RegistrationInManageSerializer
    queryset = Registration.objects.all()

    @decorators.action(detail=True)
    def messages(self, request, *args, **kwargs):
        return response.Response(MessageInRegistrationSerializer(self.get_object().messages.all(), many=True).data)

    @decorators.action(detail=True)
    def payments(self, request, *args, **kwargs):
        from pay.serializers import PaymentInRegistrationSerializer
        return response.Response(PaymentInRegistrationSerializer(self.get_object().payments.all(), many=True).data)

    @decorators.action(detail=True, methods=['POST', ])
    def new_message(self, request, *args, **kwargs):
        serializer = NewMessageFromManagerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save(registration=self.get_object())
        if message.send_sms:
            from omid_utils.sms import sendSMS
            sendSMS([message.registration.profile.mobile], message.text)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    @decorators.action(detail=True, methods=['POST', ])
    def change_status(self, request, *args, **kwargs):
        new_status = request.data.get('status', Registration.STATUS_DEFAULT)
        registration = self.get_object()
        registration.status = new_status
        registration.save()
        couple = registration.get_couple_registration()
        if couple:
            couple.status = new_status
            couple.save()
        return response.Response(RegistrationInManageSerializer(registration).data)

    @decorators.action(detail=True, methods=['POST', ])
    def change_answer(self, request, *args, **kwargs):
        question_id = request.data.get('question_id', None)
        yes = request.data.get('yes', False)
        registration = self.get_object()
        if question_id:
            Answer.objects.update_or_create(question_id=question_id, registration=registration, defaults={'yes': yes})
            couple = registration.get_couple_registration()
            if couple:
                Answer.objects.update_or_create(question_id=question_id, registration=couple,
                                                defaults={'yes': yes})
        return response.Response(RegistrationInManageSerializer(registration).data)


class ProgramManagement(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = (permissions.IsAuthenticated, IsManager)
    serializer_class = ProgramManageSerializer
    queryset = Program.objects.all()

    @decorators.action(detail=True)
    def registrations(self, request, *args, **kwargs):
        return response.Response(RegistrationInManageSerializer(self.get_object().registrations, many=True).data)

    @decorators.action(detail=True)
    def last_messages(self, request, *args, **kwargs):
        reg_ids = Message.objects.filter(to_user=False).filter(registration__program=self.get_object()).values_list(
            'registration_id', flat=True)
        registrations = Registration.objects.filter(id__in=reg_ids).exclude(status=Registration.STATUS_REMOVED)
        return response.Response(RegistrationMessageSerializer(registrations, many=True).data)

    @decorators.action(detail=True)
    def posts(self, request, *args, **kwargs):
        return response.Response(PostSerializer(self.get_object().posts.order_by('-id'), many=True).data)

    @decorators.action(detail=True, methods=['POST', ])
    def draw(self, request, *args, **kwargs):
        left_chances = int(request.data.get('chances', 0))
        registrations = self.get_object().registrations.filter(id__in=request.data.get('ids', []))
        undecided = registrations.count()
        from random import random
        for registration in registrations:
            num = left_chances / undecided
            r=random()
            win = r < num
            if win:
                left_chances -= 1
            undecided -= 1
            new_status = Registration.STATUS_CERTAIN if win else Registration.STATUS_RESERVED
            registration.status = new_status
            registration.save()
            couple = registration.get_couple_registration()
            if couple:
                couple.status = new_status
                couple.save()
        return response.Response(RegistrationInManageSerializer(self.get_object().registrations.all(), many=True).data)

    @decorators.action(detail=True, methods=['POST', ])
    def change_status(self, request, *args, **kwargs):
        new_status = request.data.get('status', Registration.STATUS_DEFAULT)
        registrations = self.get_object().registrations.filter(id__in=request.data.get('ids', []))
        for registration in registrations:
            registration.status = new_status
            registration.save()
            couple = registration.get_couple_registration()
            if couple:
                couple.status = new_status
                couple.save()
        return response.Response(RegistrationInManageSerializer(self.get_object().registrations.all(), many=True).data)

    @decorators.action(detail=True, methods=['POST', ])
    def change_answer(self, request, *args, **kwargs):
        question_id = request.data.get('question_id', None)
        yes = request.data.get('yes', False)
        registrations = self.get_object().registrations.filter(id__in=request.data.get('ids', []))
        for registration in registrations:
            if question_id:
                Answer.objects.update_or_create(question_id=question_id, registration=registration,
                                                defaults={'yes': yes})
                couple = registration.get_couple_registration()
                if couple:
                    Answer.objects.update_or_create(question_id=question_id, registration=couple,
                                                    defaults={'yes': yes})
        return response.Response(RegistrationInManageSerializer(self.get_object().registrations.all(), many=True).data)


    @decorators.action(detail=True, methods=['POST', ])
    def bulk_message(self, request, *args, **kwargs):
        text = request.data.get('text', None)
        send_sms = request.data.get('send_sms', False)
        registrations = self.get_object().registrations.filter(id__in=request.data.get('ids', []))
        if text:
            for registration in registrations:
                    Message.objects.create(text=text, registration=registration,send_sms=send_sms)
            if send_sms:
                from omid_utils.sms import sendSMS
                numbers=registrations.values_list('profile__mobile',flat=True)
                sendSMS(numbers,text)
        return response.Response('OK')


class CreatePost(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsManagerOfProgram)
    serializer_class = PostCreateSerializer


class EditPost(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsManagerOfProgram)
    serializer_class = PostSerializer

class DeletePost(generics.DestroyAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsManagerOfProgram)
