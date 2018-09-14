from rest_framework import generics, permissions, decorators, response
from .serializers import ProfileSerializer, CoupleSerializer
from .models import *


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
