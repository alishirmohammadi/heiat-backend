from rest_framework import decorators, response
from accounts.models import Profile
from program.models import Registration, Profile, Program, RegisterState


@decorators.api_view(['GET'])
def choices(request):
    ans = {
        'PEOPLE_TYPE_CHOICES': dict(Profile.PEOPLE_TYPE_CHOICES),
        'CONSCRIPTION_CHOICES': dict(Profile.CONSCRIPTION_CHOICES),
        'STATUS_CHOICES': dict(RegisterState.STATUS_CHOICES),
        'PROGRAM_TYPE_CHOICES': dict(Program.TYPE_CHOICES),
        'PROGRAM_STATE_CHOICES': dict(Program.STATE_CHOICES)
    }

    return response.Response(ans)
