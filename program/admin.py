from .models import Program, Registration, Pricing, Management, Message, Message_reciving
from pay.models import Payment
from django.contrib import admin
from .models import Management


class ManagementInline(admin.TabularInline):
    model = Management
    min_num = 0
    extra = 0
    # def show_firm_url(self, obj):
    #     return format_html("<a href='{url}'>{http://google.com}</a>", url=obj.firm_url)

        # show_firm_url.short_description = "Firm URL"

    def show_firm_url(self,obj):
        return u'<a href="/admin/program/management/{}">{}</a>'.format(obj.id,obj.profile)
    show_firm_url.allow_tags = True

    readonly_fields = ('show_firm_url' , 'role')
    exclude = ('profile','canEditProgram', 'canFilter', 'canSelect', 'canEditRegistration', 'canDocument', 'canMassage', 'canAdd',
               'documentation')
    # list_display_links = ('provider',)/\
    can_delete = False


class Program_Admin(admin.ModelAdmin):
    list_display = ['id', 'title', 'type', 'year', 'Master', 'number_of_register', 'certain_or_came', 'sum_of_money']
    inlines = [ManagementInline]
admin.site.register(Program, Program_Admin)


class Registration_Admin(admin.ModelAdmin):
    list_display = ['id', 'profile', 'program', 'registrationDate', 'coupling', 'status']


admin.site.register(Registration, Registration_Admin)



class Management_Admin(admin.ModelAdmin):
    list_display = ['id', 'program', 'profile','role']
    # form = BookForm


admin.site.register(Management, Management_Admin)


class Message_reciving_Admin(admin.ModelAdmin):
    list_display = ['id', 'message', 'registration']


admin.site.register(Message_reciving, Message_reciving_Admin)


class Message_Admin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'subject', 'content', 'sendEmail', 'sendSms', 'sendInbox', 'messageSendDate']


admin.site.register(Message, Message_Admin)


class Payment_Admin(admin.ModelAdmin):
    list_display = ['id', 'registration', 'numberOfInstallment', 'amount', 'refId', 'saleRefId', 'takingDate',
                    'success']


admin.site.register(Payment, Payment_Admin)


class Pricing_Admin(admin.ModelAdmin):
    list_display = ['id', 'program', 'Coupling', 'people_type']


admin.site.register(Pricing, Pricing_Admin)
