from django.contrib import admin
from .models import Expense
from .models import Payment

class PaymentForExpenseInline(admin.TabularInline):
    model = Payment
    readonly_fields = ('id','amount','takingDate','refId','saleRefId','success')
    exclude = ('registration', 'numberOfInstallment')
    can_delete = False

class Expense_Admin(admin.ModelAdmin):
    list_display = ['id', 'is_open', 'expense_name','sum_of_money']
    inlines = [PaymentForExpenseInline]
admin.site.register(Expense,  Expense_Admin)