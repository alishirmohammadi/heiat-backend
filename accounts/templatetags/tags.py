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