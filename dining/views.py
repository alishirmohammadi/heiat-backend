from datetime import datetime

from rest_framework import decorators, permissions, response

from accounts.models import Profile
from dining.models import Meal
from program.models import Program, Question

is_test = True
paboos = Program.objects.get(title="پابوس عشق ۹۸")
paboos_f = Program.objects.get(title="پابوس عشق فارغ التحصیلان ۹۸")
lunches = ((
               Question.objects.get(program=paboos, title="ناهار روز اول"),
               Question.objects.get(program=paboos, title="ناهار روز دوم"),
               Question.objects.get(program=paboos, title="ناهار روز سوم"),
           ), (
               Question.objects.get(program=paboos_f, title="ناهار روز اول"),
               Question.objects.get(program=paboos_f, title="ناهار روز دوم"),
               Question.objects.get(program=paboos_f, title="ناهار روز سوم"),
           ))


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
    meal = Meal.objects.filter(start_time__lte=datetime.now())
    return response.Response(username)
