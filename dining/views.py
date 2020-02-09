from datetime import datetime

from rest_framework import decorators, permissions, response

from accounts.models import Profile
from dining.models import Meal, FoodReception
from program.models import Program, Registration, Question, Answer

sadat = Question.objects.get(title="اسکان سادات", program__id=22)
shohada = Question.objects.get(title="اسکان سید الشهدا", program__id=22)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def test(request):
    return response.Response("You are logged in!")


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def receipt(request, eskan):
    username = request.data.get("username")
    if eskan != "sadat" and eskan != "shohada":
        return response.Response("", status=400)
    if not username:
        return response.Response({"message": "نام کاربری فرستاده نشده است.", "user": {}, "ok": False})
    profile = Profile.objects.filter(user__username=username).first()
    meal = Meal.objects.filter(program__id=22, start_time__lte=datetime.now(), end_time__gte=datetime.now()).first()
    if not meal:
        return response.Response({"message": "وعدهٔ غذایی در این زمان وجود ندارد", "ok": False})
    if not profile:
        return response.Response({"message": "کاربر وارد شده وجود ندارد.", "user": {}, "ok": False})
    if eskan == "sadat":
        reg = Registration.objects.filter(program=22, profile=profile, status='came').first()
        if not reg:
            return response.Response(
                {"message": "شما در این برنامه شرکت نکرده اید.", "ok": False, "user": {"name": profile.__str__()}})
        answer = Answer.objects.filter(question=sadat, registration=reg).first()
        if not answer:
            return response.Response(
                {"message": "شما در اسکان سادات نیستید", "ok": False, "user": {"name": str(profile)}})
        if not answer.yes:
            return response.Response(
                {"message": "شما در اسکان سادات نیستید", "ok": False, "user": {"name": str(profile)}})
        food_reception = FoodReception.objects.filter(meal=meal, profile=profile).first()
        if not food_reception:
            food_reception = FoodReception(meal=meal, profile=profile, status='receipt')
            food_reception.save()
            return response.Response({"message": "غذا با موفقیت دریافت شد", "ok": True, "user": {"name": str(profile)}})
        if food_reception.status == "receipt":
            return response.Response(
                {"message": "شما قبلا غذا دریافت کرده اید.", "ok": False, "user": {"name": str(profile)}})
        if food_reception.status == "cancel":
            return response.Response(
                {"message": "شما این وعدهٔ غذایی را لغو کرده اید.", "ok": False, "user": {"name": str(profile)}})
    if eskan == "shohada":
        reg = Registration.objects.filter(program__id=23, profile=profile, status='came').first()
        if reg:
            food_reception = FoodReception.objects.filter(meal=meal, profile=profile)
            if not food_reception:
                food_reception = FoodReception(meal=meal, profile=profile, status='receipt')
                food_reception.save()
                return response.Response(
                    {"message": "غذا با موفقیت دریافت شد", "ok": True, "user": {"name": str(profile)}})
            elif food_reception.status == "receipt":
                return response.Response(
                    {"message": "شما قبلا غذا دریافت کرده اید.", "ok": False, "user": {"name": str(profile)}})
            elif food_reception.status == "cancel":
                return response.Response(
                    {"message": "شما این وعدهٔ غذایی را لغو کرده اید.", "ok": False, "user": {"name": str(profile)}})
        else:
            reg = Registration.objects.filter(program__id=22, profile=profile, status='came').first()
            if not reg:
                return response.Response(
                    {"message": "شما در این برنامه شرکت نکرده اید.", "ok": False, "user": {"name": profile.__str__()}})
            answer = Answer.objects.filter(registration=reg, question=shohada).first()
            if not answer:
                return response.Response(
                    {"message": "شما در اسکان سیدالشهدا نیستید", "ok": False, "user": {"name": str(profile)}})
            if not answer.yes:
                return response.Response(
                    {"message": "شما در اسکان سیدالشهدا نیستید", "ok": False, "user": {"name": str(profile)}})
            food_reception = FoodReception.objects.filter(meal=meal, profile=profile).first()
            if not food_reception:
                food_reception = FoodReception(meal=meal, profile=profile, status='receipt')
                food_reception.save()
                return response.Response(
                    {"message": "غذا با موفقیت دریافت شد", "ok": True, "user": {"name": str(profile)}})
            elif food_reception.status == "receipt":
                return response.Response(
                    {"message": "شما قبلا غذا دریافت کرده اید.", "ok": False, "user": {"name": str(profile)}})
            elif food_reception.status == "cancel":
                return response.Response(
                    {"message": "شما این وعدهٔ غذایی را لغو کرده اید.", "ok": False, "user": {"name": str(profile)}})


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
        return response.Response(resp)
    resp['program'] = program.title
    meal = Meal.objects.filter(program=program, start_time__lte=datetime.now(), end_time__gte=datetime.now()).first()
    if not meal:
        resp['message'] = "وعده غذایی‌ای در این زمان وجود ندارد."
        return response.Response(resp)
    resp['ok'] = True
    resp['message'] = "اطلاعات ارسال شد."
    resp['meal']['title'] = meal.title
    resp['meal']['food'] = meal.food
    total = len(Registration.objects.filter(program=program, profile__gender=True, status='came'))
    total -= len(FoodReception.objects.filter(meal=meal, status='cancel'))
    resp['meal']['total'] = total
    resp['meal']['receipt_count'] = len(FoodReception.objects.filter(meal=meal, status='receipt'))

    return response.Response(resp)
