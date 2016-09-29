from django.contrib import admin
from .models import Charity,Expense
from .models import Payment

# # Register your models here.
# admin.site.register(Payment)
class Charity_Admin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'success', 'sum_of_money']
admin.site.register(Charity,  Charity_Admin)


class Expense_Admin(admin.ModelAdmin):
    list_display = ['id', 'isopen', 'payment_type','sum_of_money']
admin.site.register(Expense,  Expense_Admin)