from django import template
import itertools


register = template.Library()


@register.filter
def chunks(items, chunk_size):
    iterable = [iter(items)] * chunk_size
    return itertools.izip_longest(fillvalue=None, *iterable)
