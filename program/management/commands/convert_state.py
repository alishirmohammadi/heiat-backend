from django.core.management.base import BaseCommand, CommandError
from program.models import Program,Post
class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for program in Program.objects.all():
            if not program.isPublic:
                program.state=Program.STATE_CONFIG
            else:
                program.state=Program.STATE_ARCHIVE
            program.save()


