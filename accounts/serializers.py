from rest_framework import serializers

from .models import *


class CoupleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    name = serializers.CharField(source='user.get_full_name')

    class Meta:
        model = Profile
        fields = ('username', 'name', 'gender')


class ProfileSerializer(serializers.ModelSerializer):
    couple = CoupleSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            'mobile', 'birth_date', 'gender', 'people_type', 'student_number', 'conscription', 'father_name',
            'passport', 'passport_number', 'passport_date_of_issue', 'passport_date_of_expiry', 'couple',
            'has_management')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')


from djoser.serializers import UserCreateSerializer


class UserRegisterSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password', 'id')
