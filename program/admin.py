from django.contrib import admin

from .models import Program, Registration, Message, Question, Answer, Post


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'year', 'master', 'number_of_register', 'certain_or_came', 'sum_of_money']


admin.site.register(Program, ProgramAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'program', 'registrationDate', 'coupling', 'status']
    readonly_fields = ('profile',)
    list_filter = ['program', 'coupling', 'status', ]
    search_fields = ['profile__user__first_name', 'profile__user__last_name']

admin.site.register(Registration, RegistrationAdmin)


admin.site.register(Message)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Post)
