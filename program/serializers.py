from rest_framework import serializers
from .models import *


class ProgramListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        try:
            user = self.context.get('request').user
            if user and user.is_authenticated:
                registration = Registration.objects.filter(program=obj).filter(profile__user=user).exclude(
                    status=RegisterState.STATUS_REMOVED).first()
                if registration:
                    return registration.get_status_display()
            return None
        except:
            return None

    class Meta:
        model = Program
        fields = ('id', 'title', 'program_interval', 'register_interval', 'status')


class MessageInRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'to_user', 'text', 'send_sms', 'send_date')


class AnswerInRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'yes', 'question', 'answer_text', 'answer_file')


class RegistrationInProgramDetailSerializer(serializers.ModelSerializer):
    from pay.serializers import PaymentInRegistrationSerializer
    payments = PaymentInRegistrationSerializer(many=True)
    messages = MessageInRegistrationSerializer(many=True)
    answers = AnswerInRegistrationSerializer(many=True)

    class Meta:
        model = Registration
        fields = ('id', 'status', 'coupling', 'sum_payed', 'next_installment', 'payments', 'messages', 'answers')


class PostInProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text', 'post_date')


class QuestionInProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'title', 'desc', 'var', 'params')


class ProgramDetailSerializer(serializers.ModelSerializer):
    registration = serializers.SerializerMethodField()
    posts = PostInProgramSerializer(many=True)
    users_questions = QuestionInProgramSerializer(many=True)

    def get_registration(self, obj):
        print("boz")
        try:
            user = self.context.get('request').user
            if user and user.is_authenticated:
                registration = Registration.objects.filter(program=obj).filter(profile__user=user).exclude(
                    status=RegisterState.STATUS_REMOVED).first()
                print("salam")
                print(registration)
                if registration:
                    return RegistrationInProgramDetailSerializer(registration).data
            return None
        except Exception as E:
            print(E)
            return None

    class Meta:
        model = Program
        fields = ('id', 'title', 'program_interval', 'register_interval', 'registration', 'is_open', 'posts', 'state',
                  'has_coupling', 'users_questions')


class NewMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'registration', 'text', 'send_date', 'to_user')


class ProgramNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ('id', 'title')
