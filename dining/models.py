from django.db import models

from accounts.models import Profile
from program.models import Program


class Meal(models.Model):
    program = models.ForeignKey(Program, verbose_name="برنامه", on_delete=models.CASCADE)
    title = models.CharField(verbose_name="عنوان", max_length=100)
    food = models.CharField(verbose_name="غذا", null=True, blank=True, max_length=100)
    start_time = models.DateTimeField(verbose_name="زمان شروع توزیع")
    end_time = models.DateTimeField(verbose_name="زمان پایان توزیع")


class FoodReception(models.Model):
    STATUS_CHOICES = (
        ('receipt', 'دریافت کرده'),
        ('cancel', 'لغو کرده'),
        ('reserved', 'رزرو کرده'),
    )

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name="وعدهٔ غذایی")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="کاربر")
    status = models.CharField(verbose_name="وضعیت", choices=STATUS_CHOICES, max_length=20)
    reception_time = models.DateTimeField("زمان دریافت", auto_now_add=True)
