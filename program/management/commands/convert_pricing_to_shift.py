from django.core.management.base import BaseCommand, CommandError
from program.models import Program, PriceShift


class Command(BaseCommand):
    args = '<from_date offset ...>'
    help = 'Fetches the CrossRef metadata'

    # see https://github.com/CrossRef/rest-api-doc/blob/master/rest_api.md

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        for program in Program.objects.all():
            min_pricing = 1000000000
            for pricing in program.pricings():
                if pricing.sum_prices() < min_pricing:
                    min_pricing=pricing.sum_prices()
            program.base_price=min_pricing
            program.save()
            for pricing in program.pricings():
                if pricing.sum_prices() > min_pricing:
                    shift=pricing.sum_prices()-min_pricing
                    PriceShift.objects.get_or_create(program=program,people_type=pricing.people_type,defaults={'shift':shift})
            for pricing in program.pricings():
                if pricing.price2 and pricing.price2 >0:
                    program.max_first_installment=pricing.price1
                    program.save()
                    break

