from rest_framework import serializers
from .models import *


class ManagementListSerializer(serializers.ModelSerializer):
    program = serializers.StringRelatedField()
    role = serializers.CharField(source='get_role_display')

    class Meta:
        model = Management
        fields = ('id', 'program', 'role')
