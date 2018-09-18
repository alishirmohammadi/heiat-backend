from .models import Program, Registration,Message,Question,Answer,Post
from django.contrib import admin


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'year', 'master', 'number_of_register', 'certain_or_came', 'sum_of_money']


admin.site.register(Program, ProgramAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'program', 'registrationDate', 'coupling', 'status']
    readonly_fields = ('profile',)

admin.site.register(Registration, RegistrationAdmin)


admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Post)
