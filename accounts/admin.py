from django.contrib import admin
from .models import Profile
from manage_app.models import Management
from django.utils.safestring import mark_safe


class ManagementInline(admin.TabularInline):
    model = Management
    min_num = 0
    extra = 1

    def manager_url(self, obj):
        return mark_safe(u'<a href="/admin/program/management/{}">{}</a>'.format(obj.id, obj.program))

    readonly_fields = ('manager_url',)
    exclude = (
        'canEditProgram', 'canFilter', 'canSelect', 'canMessage', 'canEditRegistration',
        'canAdd', 'documentation')
    can_delete = False


class ProfileAdmin(admin.ModelAdmin):
    def user_url(self, obj):
        return mark_safe(u'<a href="/admin/auth/user/{}/change/">{}</a>'.format(obj.user.id, obj.user.username))

    list_display = ['__str__', 'user_url']
    inlines = [ManagementInline]
    search_fields = ('user__first_name', 'user__last_name', 'user__username',)
    readonly_fields = ('user',)


admin.site.register(Profile, ProfileAdmin)
