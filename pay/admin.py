from django.contrib import admin

from .models import Expense
from .models import Payment


class PaymentForExpenseInline(admin.TabularInline):
    model = Payment
    readonly_fields = ('id', 'amount', 'takingDate', 'refId', 'saleRefId', 'success')
    exclude = ('registration', 'numberOfInstallment')
    can_delete = False


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_open', 'expense_name', 'sum_of_money']
    inlines = [PaymentForExpenseInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'registration', 'numberOfInstallment', 'amount', 'refId', 'saleRefId', 'takingDate',
                    'success']
    list_filter = ['registration__program_id', 'expense', 'success']
    readonly_fields = ['optional_name', 'optional_mobile', 'registration']
