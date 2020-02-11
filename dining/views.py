from datetime import datetime

from rest_framework import decorators, permissions, response

from accounts.models import Profile
from dining.models import Meal, FoodReception
from program.models import Program, Registration, Question, Answer

sadat = Question.objects.get(title="اسکان سادات", program__id=22)
shohada = Question.objects.get(title="اسکان سید الشهدا", program__id=22)
blanket_meal = Meal.objects.get(title="پتو", program__id=22)
book_meal = Meal.objects.get(title="بن کتاب", program__id=22)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def test(request):
    return response.Response("You are logged in!")


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def receipt(request, eskan, meal=None):
    username = request.data.get("username")
    if eskan != "sadat" and eskan != "shohada":
        return response.Response("", status=400)
    if not username:
        return response.Response({"message": "نام کاربری فرستاده نشده است.", "user": {}, "ok": False})
    profile = Profile.objects.filter(user__username=username).first()
    if not meal:
        meal = Meal.objects.filter(program__id=22, start_time__lte=datetime.now(), end_time__gte=datetime.now()).first()
    if not meal:
        return response.Response({"message": "وعدهٔ غذایی در این زمان وجود ندارد", "ok": False})
    if not profile:
        return response.Response({"message": "کاربر وارد شده وجود ندارد.", "user": {}, "ok": False})
    if eskan == "sadat":
        reg = Registration.objects.filter(program=22, profile=profile, status='came', coupling=False).first()
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
        reg = Registration.objects.filter(program__id=23, profile=profile, status='came', coupling=False).first()
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
            reg = Registration.objects.filter(program__id=22, profile=profile, status='came', coupling=False).first()
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
def status(request, eskan, meal=None):
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
    if eskan != "sadat" and eskan != "shohada":
        return response.Response("", status=400)
    if not meal:
        meal = Meal.objects.filter(program__id=22, start_time__lte=datetime.now(), end_time__gte=datetime.now()).first()
    if not meal:
        resp["message"] = "وعدهٔ غذایی در این زمان یافت نشد."
        return response.Response(resp)
    resp['meal']['title'] = meal.title
    resp['meal']['food'] = meal.food
    resp['message'] = "اطلاعات ارسال شد."
    resp['ok'] = True
    resp['program'] = Program.objects.filter(id=22).first().title
    total = 0
    receipt_count = 0
    if eskan == "sadat":
        regs = Registration.objects.filter(status='came', program__id=22, coupling=False)
        for reg in regs:
            ans = Answer.objects.filter(registration=reg, question=sadat).first()
            if not ans:
                continue
            if ans.yes:
                food_receipt = FoodReception.objects.filter(profile=reg.profile, meal=meal).first()
                if not food_receipt:
                    total += 1
                elif food_receipt.status == 'receipt':
                    total += 1
                    receipt_count += 1
    elif eskan == "shohada":
        regs = Registration.objects.filter(status='came', program__id=23, coupling=False)
        for reg in regs:
            food_receipt = FoodReception.objects.filter(profile=reg.profile, meal=meal).first()
            if not food_receipt:
                total += 1
            elif food_receipt.status == 'receipt':
                total += 1
                receipt_count += 1
        regs = Registration.objects.filter(status='came', program__id=22, coupling=False)
        for reg in regs:
            ans = Answer.objects.filter(registration=reg, question=shohada).first()
            if not ans:
                continue
            if ans.yes:
                food_receipt = FoodReception.objects.filter(profile=reg.profile, meal=meal).first()
                if not food_receipt:
                    total += 1
                elif food_receipt.status == 'receipt':
                    total += 1
                    receipt_count += 1
    resp['meal']['total'] = total
    resp['meal']['receipt_count'] = receipt_count
    return response.Response(resp)


def receipt_no_eskan(request, meal=None):
    username = request.data.get("username")
    if not username:
        return response.Response({"message": "نام کاربری فرستاده نشده است.", "user": {}, "ok": False})
    profile = Profile.objects.filter(user__username=username).first()
    if not meal:
        return response.Response({"message": "امکان تحویل دادن وجود ندارد.", "ok": False})
    if not profile:
        return response.Response({"message": "کاربر وارد شده وجود ندارد.", "user": {}, "ok": False})
    reg = Registration.objects.filter(program__id=22, profile=profile, status='came', coupling=False)
    if not reg:
        reg = Registration.objects.filter(program__id=23, profile=profile, status='came', coupling=False)
    if not reg:
        return response.Response(
            {"message": "شما در این برنامه شرکت نکرده اید.", "user": {"name": str(profile)}, "ok": False})
    reception = FoodReception.objects.filter(meal=meal, profile=profile).first()
    if not reception:
        reception = FoodReception(meal=meal, profile=profile, status='receipt')
        reception.save()
        return response.Response({"message": "تحویل با موفقیت انجام شد.", "user": {"name": str(profile)}, "ok": True})
    return response.Response(
        {"message": "شما قبلا تحویل گرفته اید.", "user": {"name": str(profile)}, "ok": False})


def history_with_no_eskan(request, meal=None):
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
    if not meal:
        resp["message"] = "چیزی برای نمایش آمار در این زمان یافت نشد."
        return response.Response(resp)
    resp['meal']['title'] = meal.title
    resp['meal']['food'] = meal.food
    resp['message'] = "اطلاعات ارسال شد."
    resp['ok'] = True
    resp['program'] = Program.objects.filter(id=22).first().title
    total = 0
    receipt_count = len(FoodReception.objects.filter(meal=meal, status='receipt'))
    total += len(Registration.objects.filter(status='came', program__id=22, coupling=False))
    total += len(Registration.objects.filter(status='came', program__id=23, coupling=False))
    total -= len(FoodReception.objects.filter(meal=meal, status='cancel'))
    resp['meal']['total'] = total
    resp['meal']['receipt_count'] = receipt_count
    return response.Response(resp)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def blanket(request):
    return receipt_no_eskan(request, blanket_meal)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAdminUser,))
def blanket_history(request):
    return history_with_no_eskan(request, blanket_meal)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def book(request):
    return receipt_no_eskan(request, book_meal)


@decorators.api_view(['GET'])
@decorators.permission_classes((permissions.IsAdminUser,))
def book_history(request):
    return history_with_no_eskan(request, book_meal)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def cancel(requset, meal_id):
    meal = Meal.objects.filter(id=meal_id).first()
    if not meal:
        return response.Response({"ok": False, "message": "Meal not found"})
    food_receipt = FoodReception.objects.filter(meal=meal, profile=requset.user.profile).first()
    if food_receipt:
        return response.Response({"ok": False, "message": ""}, status=403)
    food_receipt = FoodReception(meal=meal, profile=requset.user.profile, status="cancel")
    food_receipt.save()
    return response.Response({"ok": True, "message": "Canceled"})
