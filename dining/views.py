from datetime import datetime

from rest_framework import decorators, permissions, response

from accounts.models import Profile
from dining.models import Meal, FoodReception
from program.models import Program, Registration


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def test(request):
    return response.Response("You are logged in!")


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def receipt(request, program_id):
    username = request.data.get("username")
    if not username:
        return response.Response("نام کاربری فرستاده نشده است.", status=401)
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return response.Response("کاربر وارد شده وجود ندارد.", status=404)
    program = Program.objects.filter(id=program_id).first()
    if not program:
        return response.Response("برنامه درخواست شده وجود ندارد.", status=404)
    meal = Meal.objects.filter(program=program, start_time__lte=datetime.now(), end_time__gte=datetime.now())
    if not meal:
        return response.Response("وعده غذایی‌ای در این زمان وجود ندارد.")
    registration = Registration.objects.filter(profile=profile, program=program, status='certain').first()
    if not registration:
        return response.Response("شما در این برنامه شرکت نکرده اید.", status=403)
    reception = FoodReception.objects.filter(meal=meal, profile=profile).first()
    if not reception:
        reception = FoodReception(meal=Meal, profile=profile, type='receipt')
        reception.save()
        return response.Response("دریافت غذا با موفقیت انجام شد", status=200)
    if reception.type == "reserved":
        reception.type = "receipt"
        reception.save()
        return response.Response("دریافت غذا با موفقیت انجام شد", status=200)
    elif reception.type == "receipt":
        return response.Response("قبلا غذا دریافت نموده اید.", status=403)
    elif reception.type == "cancel":
        return response.Response("رزرو غذای خود را لغو کرده بودید.", status=403)
    return response.Response(username)
