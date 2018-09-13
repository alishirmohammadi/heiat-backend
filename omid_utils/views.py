from rest_framework import decorators, response
from accounts.models import Profile
from program.models import Registration


@decorators.api_view(['GET'])
def choices(request):
    ans = {
        'PEOPLE_TYPE_CHOICES': dict(Profile.PEOPLE_TYPE_CHOICES),
        'CONSCRIPTION_CHOICES': dict(Profile.CONSCRIPTION_CHOICES),
        'STATUS_CHOICES': dict(Registration.STATUS_CHOICES)
    }

    return response.Response(ans)
