from django.core.paginator import Paginator
import requests

def chunked_iterator(queryset, chunk_size=256):
    paginator = Paginator(queryset, chunk_size)
    i = 1
    for page in range(1, paginator.num_pages + 1):
        print(i)
        i += 1
        for obj in paginator.page(page).object_list:
            yield obj


def omid_chunk_iterator(queryset, chunk_size=100, field='id', start=0, end=None):
    if not end:
        end = queryset.order_by('-' + field).first().id
    for i in range(0, int((end - start) / chunk_size + 1)):
        print(i)
        q = {
            field + '__gt': i * chunk_size + start,
            field + '__lte': (i + 1) * chunk_size + start,
        }
        chunk = queryset.filter(**q)
        for obj in chunk:
            yield obj
