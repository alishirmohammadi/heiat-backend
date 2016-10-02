from django.contrib import admin
from .models import Expense
from .models import Payment


class Expense_Admin(admin.ModelAdmin):
    list_display = ['id', 'is_open', 'expense_name','sum_of_money']
admin.site.register(Expense,  Expense_Admin)