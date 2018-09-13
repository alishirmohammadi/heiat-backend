from .models import *
from rest_framework import serializers


class ProfileInUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('mobile', 'birth_date')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileInUserSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')
