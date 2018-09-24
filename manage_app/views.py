from rest_framework import generics, views, decorators, response, permissions, viewsets, mixins,status
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
    serializer_class = RegistrationDetailManageSerializer
    queryset = Registration.objects.all()

    @decorators.action(detail=True,methods=['POST',])
    def new_message(self, request, *args, **kwargs):
        serializer = NewMessageFromManagerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message=serializer.save(registration=self.get_object())
        if message.send_sms:
            from omid_utils.sms import sendSMS
            sendSMS([message.registration.profile.mobile],message.text)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED)


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
        return response.Response(PostSerializer(self.get_object().posts, many=True).data)


class CreatePost(generics.CreateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsManagerOfProgram)
    serializer_class = PostCreateSerializer


class EditPost(generics.UpdateAPIView):
    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsManagerOfProgram)
    serializer_class = PostSerializer
