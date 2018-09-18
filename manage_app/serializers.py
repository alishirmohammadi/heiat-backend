from rest_framework import serializers
from .models import *
from program.serializers import ProgramNestedSerializer


class ManagementListSerializer(serializers.ModelSerializer):
    program = ProgramNestedSerializer()
    role = serializers.CharField(source='get_role_display')

    class Meta:
        model = Management
        fields = ('id', 'program', 'role')
