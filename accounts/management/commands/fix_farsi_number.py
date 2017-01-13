from django.core.management.base import BaseCommand, CommandError
from accounts.models import Profile
from django.contrib.auth.models import User

class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        from program.utils import farsiNumber
        profiles=Profile.objects.all()
        for p in profiles:
            try:
                print(p.studentNumber)
                p.studentNumber=farsiNumber(p.studentNumber)
                p.save()
                print(p.studentNumber)
            except:
                print("error")
            u=p.user
            u.username=farsiNumber(u.username)
            u.save()