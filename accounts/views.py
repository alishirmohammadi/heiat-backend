import random
from datetime import datetime

from rest_framework import generics, permissions, decorators, response

from omid_utils.sms import sendSMS
from omid_utils.specifics import check_melli_code
from .models import *
from .serializers import ProfileSerializer, CoupleSerializer

RESET_PASSWORD_SMS_TEXT = "رمز عبور جدید شما: %s"
RESET_PASSWORD_LIMIT_TIME = 300


class EditProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAuthenticated,))
def set_couple(request):
    melli_code = request.data.get('melli_code')
    me = request.user.profile
    print(me)
    if not melli_code:
        return response.Response('کد ملی همسر الزامی است', status=400)
    from omid_utils.specifics import check_melli_code
    if not check_melli_code(melli_code):
        return response.Response('فرمت کد ملی درست نیست', status=400)
    profile = Profile.objects.filter(user__username=melli_code).first()
    if not profile:
        return response.Response('همسر شما در سامانه حساب کاربری تشکیل نداده است', status=400)
    if me.gender == profile.gender:
        return response.Response('ازدواج با همجنس در اسلام مجاز نیست', status=400)
    if profile.couple and profile.couple.user.username != me.user.username:
        return response.Response('همسر شما همسر دیگری دارد', status=400)
    me.couple = profile
    me.save()
    profile.couple = me
    profile.save()
    return response.Response(CoupleSerializer(profile).data)


@decorators.api_view(['POST'])
def password_reset(request):
    username = request.data.get('username')
    if not username:
        return response.Response('کد ملی الزامی است', status=400)
    if not check_melli_code(username):
        return response.Response('فرمت کد ملی درست نیست', status=400)
    user = User.objects.filter(username=username)
    if not user:
        return response.Response("این نام کاربری در سایت وجود ندارد.", status=404)
    user = user[0]
    if not user.profile:
        return response.Response("شما هنوز پروفایل ندارید. لطفا با مدیر سایت تماس بگیرید.", status=404)
    if not user.profile.mobile:
        user.set_password(user.username)
        user.save()
        return response.Response("شماره موبایل شما در سیستم موجود نیست. رمز عبور شما به کد ملی تغییر کرد.", status=200)
    if datetime.now().timestamp() - user.last_login.timestamp() < RESET_PASSWORD_LIMIT_TIME:
        return response.Response("در فاصلهٔ زمانی کمتر از ۵ دقیقه امکان بازیابی رمز عبور وجود ندارد.", status=400)
    mobile = user.profile.mobile
    new_password = str(random.randrange(10000, 100000))
    user.set_password(new_password)
    user.last_login = datetime.now()
    user.save()
    sendSMS([mobile], RESET_PASSWORD_SMS_TEXT % new_password)
    mobile = mobile[:4] + "xxx" + mobile[7:]
    return response.Response("رمز عبور جدید به شمارهٔ %s ارسال شد" % mobile, status=200)


@decorators.api_view(['POST'])
@decorators.permission_classes((permissions.IsAdminUser,))
def user_detail_paboos(request):
    username = request.data.get("username")
    if not username:
        return response.Response({"message": "نام کاربری فرستاده نشده است.", "ok": False})
    profile = Profile.objects.filter(user__username=username).first()
    if not profile:
        return response.Response({"message": "کاربر وارد شده وجود ندارد.", "ok": False})
    return response.Response({
        "ok": True,
        "message": "اطلاعات ارسال شد.",
        "user": {
            "name": profile.__str__(),
            "mobile": profile.mobile,
            "gender": profile.get_gender_display(),
            "train": -1,
            "wagon": -1,
            "coupe": -1,
            "father_name": profile.father_name,
        }
    })
