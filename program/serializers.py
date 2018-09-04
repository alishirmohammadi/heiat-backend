from rest_framework import serializers
from .models import *

class ProgramListSerializer(serializers.ModelSerializer):
    class Meta:
        model=Program
        fields=('id','title','program_interval','register_interval')