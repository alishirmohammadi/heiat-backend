from django.contrib import admin
from .models import *


class ManagementAdmin(admin.ModelAdmin):
    list_display = ['id', 'program', 'profile', 'role']


admin.site.register(Management, ManagementAdmin)