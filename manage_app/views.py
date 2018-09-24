from rest_framework import generics, views, decorators, response, permissions, viewsets, mixins
from .models import *
from .serializers import *
from .pemissions import *


class ManagementList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ManagementListSerializer

    def get_queryset(self):
        return self.request.user.profile.managements.all()


class ProgramManagement(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    permission_classes = (permissions.IsAuthenticated, IsManager)
    serializer_class = ProgramManageSerializer
    queryset = Program.objects.all()

    @decorators.action(detail=True)
    def registrations(self, request, *args, **kwargs):
        return response.Response(RegistrationInManageSerializer(self.get_object().registrations, many=True).data)

    @decorators.action(detail=True)
    def last_messages(self, request, *args, **kwargs):
        reg_ids = Message.objects.filter(to_user=False).filter(registration__program=self.get_object()).values_list('registration_id', flat=True)
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
