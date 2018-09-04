from django.core.management.base import BaseCommand, CommandError
from program.models import Program, Question, Answer


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for program in Program.objects.all():
            if program.additionalOption:
                question = Question.objects.create(program=program, title=program.additionalOption, user_sees=True)
                for registration in program.registration_set.all():
                    Answer.objects.create(question=question, registration=registration,
                                          yes=registration.additionalOption)
