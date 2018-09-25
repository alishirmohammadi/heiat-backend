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
        fields = ('id', 'title', 'desc', 'user_sees', 'shift')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'text', 'post_date')


class UserInProfileInManageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name')

    class Meta:
        model = User
        fields = ('username', 'name', 'email')


class ProfileInRegistrationListInProgramManageSerializer(serializers.ModelSerializer):
    user = UserInProfileInManageSerializer(read_only=True)
    passport_status = serializers.CharField(source='get_passport_display')

    class Meta:
        model = Profile
        fields = (
            'user', 'gender', 'people_type', 'student_number', 'conscription', 'passport_status', 'passport_number',
            'passport_date_of_issue', 'passport_date_of_expiry', 'father_name', 'mobile', 'birth_date')


class RegistrationInManageSerializer(serializers.ModelSerializer):
    answers = AnswerInRegistrationSerializer(many=True)
    profile = ProfileInRegistrationListInProgramManageSerializer()

    class Meta:
        model = Registration
        fields = ('id', 'profile', 'status', 'coupling', 'answers', 'numberOfPayments', 'registrationDate', 'couple_id')


class ProgramManageSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Program
        fields = ('id', 'title', 'program_interval', 'register_interval', 'is_open', 'state',
                  'has_coupling', 'questions', 'type', 'year','base_price','max_first_installment','max_second_installment')


class MessageInManageInboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('text', 'send_date')


class RegistrationMessageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='profile.user.get_full_name')
    message = MessageInManageInboxSerializer(read_only=True, source='last_from_user_message')

    class Meta:
        model = Registration
        fields = ('id', 'name', 'message')


class NewMessageFromManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'send_date', 'to_user', 'send_sms')


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'text', 'post_date', 'program')


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'desc', 'user_sees', 'program', 'shift')


class PriceShiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceShift
        fields = ('people_type', 'shift')
