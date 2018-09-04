from django.core.management.base import BaseCommand, CommandError
from program.models import Message, Message2, Message_reciving
from django.utils.html import strip_tags


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for mr in Message_reciving.objects.filter(message__sendInbox=True):
            text = strip_tags(mr.message.content).strip()
            if not text:
                text = mr.message.subject.strip()
            if text:
                new_message = Message2()
                new_message.text = text
                new_message.send_sms = mr.message.sendSms
                new_message.registration = mr.registration
                new_message.send_date = mr.message.messageSendDate
                new_message.save()
