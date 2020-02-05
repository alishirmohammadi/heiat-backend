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
        return response.Response({"message": "نام کاربری فرستاده نشده است.", "ok": False}, status=400)
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return response.Response({"message": "کاربر وارد شده وجود ندارد.", "ok": False}, status=404)
    program = Program.objects.filter(id=program_id).first()
    if not program:
        return response.Response({"message": "برنامه درخواست شده وجود ندارد.", "ok": False}, status=404)
    meal = Meal.objects.filter(program=program, start_time__lte=datetime.now(), end_time__gte=datetime.now()).first()
    if not meal:
        return response.Response({"message": "وعده غذایی‌ای در این زمان وجود ندارد.", "ok": False}, status=404)
    registration = Registration.objects.filter(profile=profile, program=program, status='certain').first()
    if not registration:
        return response.Response({"message": "شما در این برنامه شرکت نکرده اید.", "ok": False}, status=403)
    reception = FoodReception.objects.filter(meal=meal, profile=profile).first()
    if not reception:
        reception = FoodReception(meal=meal, profile=profile, status='receipt')
        reception.save()
        return response.Response({"message": "دریافت غذا با موفقیت انجام شد", "ok": True}, status=200)
    if reception.status == "reserved":
        reception.status = "receipt"
        reception.save()
        return response.Response({"message": "دریافت غذا با موفقیت انجام شد", "ok": True}, status=200)
    elif reception.status == "receipt":
        return response.Response({"message": "قبلا غذا دریافت نموده اید.", "ok": False}, status=403)
    elif reception.status == "cancel":
        return response.Response({"message": "رزرو غذای خود را لغو کرده بودید.", "ok": False}, status=403)
    return response.Response({"message": "خطای ناشناس", "ok": False}, status=406)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAdminUser,))
def status(request, program_id):
    resp = {
        "ok": False,
        "message": "برنامه درخواست شده وجود ندارد.",
        "program": "",
        "meal": {
            "title": "",
            "food": "",
            "total": 0,
            "receipt_count": 0
        }
    }
    program = Program.objects.filter(id=program_id).first()
    if not program:
        return response.Response(resp, status=404)
    resp['program'] = program.title
    meal = Meal.objects.filter(program=program, start_time__lte=datetime.now(), end_time__gte=datetime.now()).first()
    if not meal:
        resp['message'] = "وعده غذایی‌ای در این زمان وجود ندارد."
        return response.Response(resp, status=404)
    resp['ok'] = True
    resp['message'] = "اطلاعات ارسال شد."
    resp['meal']['title'] = meal.title
    resp['meal']['food'] = meal.food
    total = len(Registration.objects.filter(program=program, profile__gender=True, status='came'))
    total -= len(FoodReception.objects.filter(meal=meal, status='cancel'))
    resp['meal']['total'] = total
    resp['meal']['receipt_count'] = len(FoodReception.objects.filter(meal=meal, status='receipt'))

    return response.Response(resp, status=200)
