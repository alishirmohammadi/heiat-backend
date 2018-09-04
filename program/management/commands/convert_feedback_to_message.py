from django.core.management.base import BaseCommand, CommandError
from program.models import Message, Message2, Message_reciving,Registration
from django.utils.html import strip_tags


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for reg in Registration.objects.filter(feedBack__isnull=False):
            if reg.feedBack.strip() and reg.feedBack.strip() != 'None':
                Message2.objects.create(text=reg.feedBack,registration=reg,to_user=False)
