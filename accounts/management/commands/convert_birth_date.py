from django.core.management.base import BaseCommand, CommandError
from accounts.models import Profile
from django.contrib.auth.models import User
from omid_utils.jalali import Persian
class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for profile in Profile.objects.all():
            if profile.is_birth_valid():
                if len(str(profile.birthYear))==2:
                    year=1300+profile.birthYear
                else:
                    year=profile.birthYear
                try:
                    profile.birth_date=Persian(year,profile.birthMonth,profile.birthDay).gregorian_datetime()
                    profile.save()
                except:
                    print(str(year))
                    print(str(profile.birthMonth))
                    print(str(profile.birthDay))


