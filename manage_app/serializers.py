from rest_framework import serializers
from .models import *
from program.serializers import *


class ManagementListSerializer(serializers.ModelSerializer):
    program = ProgramNestedSerializer()
    role = serializers.CharField(source='get_role_display')

    class Meta:
        model = Management
        fields = ('id', 'program', 'role')


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'desc', 'user_sees')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'text', 'post_date')


class ProfileInRegistrationListInProgramManageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = Profile
        fields = ('name', 'gender','people_type')


class RegistrationInProgramManageSerializer(serializers.ModelSerializer):
    answers = AnswerInRegistrationSerializer(many=True)
    profile = ProfileInRegistrationListInProgramManageSerializer()

    class Meta:
        model = Registration
        fields = ('id', 'profile', 'status', 'coupling', 'answers')


class ProgramManageSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    questions = QuestionSerializer(many=True, read_only=True)
    registrations = RegistrationInProgramManageSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ('id', 'title', 'program_interval', 'register_interval', 'is_open', 'state',
                  'has_coupling', 'questions', 'posts','registrations')
