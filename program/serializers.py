from rest_framework import serializers
from .models import *


class ProgramListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        try:
            user = self.context.get('request').user
            if user and user.is_authenticated:
                registration = Registration.objects.filter(program=obj).filter(profile__user=user).exclude(
                    status=Registration.STATUS_REMOVED).first()
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


class RegistrationInProgramDetailSerializer(serializers.ModelSerializer):
    from pay.serializers import PaymentInRegistrationSerializer
    payments = PaymentInRegistrationSerializer(many=True)
    messages=MessageInRegistrationSerializer(many=True)

    class Meta:
        model = Registration
        fields = ('id', 'status', 'payments','messages')


class PostInProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('text', 'post_date')


class ProgramDetailSerializer(serializers.ModelSerializer):
    registration = serializers.SerializerMethodField()
    posts = PostInProgramSerializer(many=True)

    def get_registration(self, obj):
        try:
            user = self.context.get('request').user
            if user and user.is_authenticated:
                registration = Registration.objects.filter(program=obj).filter(profile__user=user).exclude(
                    status=Registration.STATUS_REMOVED).first()
                if registration:
                    return RegistrationInProgramDetailSerializer(registration).data
            return None
        except:
            return None

    class Meta:
        model = Program
        fields = ('id', 'title', 'program_interval', 'register_interval', 'registration', 'is_open', 'posts')
