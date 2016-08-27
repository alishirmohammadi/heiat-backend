from django import template
from program.models import Program
register = template.Library()


@register.filter
def get_tuple_item(tup, key):
    dicti = dict(tup)
    return dicti[key]

@register.filter
def get_keys(tup):
    dicti = dict(tup)
    keys=dicti.keys()
    return keys
@register.assignment_tag()
def get_tuple():
    month = {1: 'فروردین', 2: 'اردیبهشت', 3: 'خرداد', 4: 'تیر', 5: 'مرداد', 6: 'شهریور', 7: 'مهر', 8: 'آبان', 9: 'آذر',
             10: 'دی', 11: 'بهمن', 12: 'اسفند'}
    return month
@register.assignment_tag
def get_lastProg():
    lastProg = Program.objects.filter(isPublic=True).last()
    return lastProg



        # @register.filter
# def get_metadata_filter(doi):
#     from search.lib.metadata_utils import get_metadata
#     metadata=get_metadata(doi)
#     return metadata

# @register.filter
# def get_limit(university, type):
#     field_name=type+'_limit'
#     limit=getattr(university,field_name)
#     return limit