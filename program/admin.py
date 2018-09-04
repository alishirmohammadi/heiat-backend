from .models import Program, Registration, Management
from django.contrib import admin
from .models import Management
from django.utils.safestring import mark_safe

class ManagementInline(admin.TabularInline):
    model = Management
    min_num = 0
    extra = 0
    # def show_firm_url(self, obj):
    #     return format_html("<a href='{url}'>{http://google.com}</a>", url=obj.firm_url)

    # show_firm_url.short_description = "Firm URL"

    def manager_url(self, obj):
        return mark_safe(u'<a href="/admin/program/management/{}">{}</a>'.format(obj.id, obj.profile))


    readonly_fields = ('manager_url',)
    exclude = (
        'canEditProgram', 'canFilter', 'canSelect', 'canEditRegistration', 'canDocument', 'canMessage',
        'canAdd',
        'documentation')
    # list_display_links = ('provider',)/\
    can_delete = False


class Program_Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'year', 'master', 'number_of_register', 'certain_or_came', 'sum_of_money']
    inlines = [ManagementInline]


admin.site.register(Program, Program_Admin)



class Registration_Admin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'program', 'registrationDate', 'coupling', 'status']


admin.site.register(Registration, Registration_Admin)


class Management_Admin(admin.ModelAdmin):
    list_display = ['id', 'program', 'profile', 'role']
    # form = BookForm


admin.site.register(Management, Management_Admin)

