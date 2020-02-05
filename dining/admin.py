from django.contrib import admin

from dining.models import *


@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ['title', 'food', 'program', 'start_time', 'end_time']
    list_filter = ['program']


@admin.register(FoodReception)
class FoodReceptionAdmin(admin.ModelAdmin):
    list_display = ['meal', 'profile', 'status', 'reception_time']
    list_filter = ['meal']
    readonly_fields = ['profile']
