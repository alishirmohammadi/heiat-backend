from datetime import datetime

from rest_framework import decorators, permissions, response

from accounts.models import Profile
from dining.models import Meal
from program.models import Program


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
    meal = Meal.objects.filter(program=program, start_time__lte=datetime.now(), end_gte=datetime.now())
    if not meal:
        return response.Response("وعده غذایی‌ای با اطلاعات وارد شده وجود ندارد. ")
    return response.Response(username)
