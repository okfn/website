from django import template
import itertools

register = template.Library()
    

@register.filter
def split_rows(objects, columns):
    if len(objects) == 0:
        return objects

    return itertools.izip_longest(*[iter(objects)]*columns)

