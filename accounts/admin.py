from django.contrib import admin
from .models import Profile
from program.models import Management

# Register your models here.

class ManagementInline(admin.TabularInline):

    model = Management
    min_num = 0
    extra = 1
    # def show_firm_url(self, obj):
    #     return format_html("<a href='{url}'>{http://google.com}</a>", url=obj.firm_url)

    # show_firm_url.short_description = "Firm URL"

    def manager_url(self, obj):
        return u'<a href="/admin/program/management/{}">{}</a>'.format(obj.id, obj.profile)

    manager_url.allow_tags = True

    readonly_fields = ('manager_url',)
    exclude = (
         'canEditProgram', 'canFilter', 'canSelect','canMessage', 'canEditRegistration', 'canDocument',
        'canAdd',
        'documentation')
    can_delete = False


class ProfileAdmin(admin.ModelAdmin):
    def user_url(self, obj):
        return u'<a href="/admin/auth/user/{}/change/">{}</a>'.format(obj.user.id, obj.user.username)
    user_url.allow_tags=True
    list_display = [ '__str__', 'user_url']
    inlines = [ManagementInline]
    search_fields = ('user__first_name', 'user__last_name', 'user__username', )

admin.site.register(Profile,ProfileAdmin)